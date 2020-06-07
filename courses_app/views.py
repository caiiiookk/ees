from django import views
from django.shortcuts import render, redirect, Http404
from django.urls import resolve
from users_app.permissions import has_admin_permission
from django.core.exceptions import PermissionDenied
from .forms import (
    EditCourseForm,
    EditSectionForm,
    EditDocumentForm,
    EditPageForm,
    EditTestForm,
    EditQuestionForm,
    EditAnswerForm,
    UserQuestionCheckForm,
    UserQuestionFileForm,
    UserQuestionInputForm,
    UserQuestionRadioForm,
    EmployeeRateForm,
)
from .models import (
    CourseModel,
    Course2Employee,
    Course2Student,
    Course2Teacher,
    SectionModel,
    Section2Sections,
    DocumentsModel,
    PagesModel,
    TestsModel,
    QuestionModel,
    CheckOrRadioAnswerModel,
    Question2Group,
    TriesModel,
    Try2Question,
    User,
)


# Create your views here.

def get_try_rating(try_entry):
    answer = Try2Question.objects.filter(try_field=try_entry).order_by('id')
    answer_rating = sum(answer.values_list('rate', flat=True))
    max_rating = sum(answer.values_list('question__rating', flat=True))
    return answer_rating, max_rating


def get_section_by_url(curr_section, url):
    urls = str(url).split('/')
    if urls.__len__() < 5:
        return curr_section
    if urls[-1] == '':
        urls = urls[:-1]
    sections_w_ids = urls[4:]
    section_ids = sections_w_ids[1::2]
    try:
        for index, section_id in enumerate(section_ids):
            if sections_w_ids[index * 2] != 'section':
                break
            curr_section = SectionModel.objects.filter(
                section_of_this_section__in=Section2Sections.objects.filter(section=curr_section))[int(section_id) - 1]
    except:
        raise Http404
    return curr_section


def has_access_to_teacher_course(user, course):
    return True


def has_access_to_student_course(user, course):
    return True


def has_access_to_employee_course(user, course):
    return True


def teacher_page_start(request, course_id):
    try:
        course = CourseModel.objects.get(id=course_id)
    except CourseModel.DoesNotExist:
        raise Http404
    has_access = has_access_to_teacher_course(request.user, course)
    if not has_access:
        raise PermissionDenied
    curr_section = get_section_by_url(course.section, request.get_full_path())
    return course, curr_section


def employee_page_start(request, course_id):
    try:
        course = CourseModel.objects.get(id=course_id)
    except CourseModel.DoesNotExist:
        raise Http404
    has_access = has_access_to_employee_course(request.user, course)
    if not has_access:
        raise PermissionDenied
    curr_section = get_section_by_url(course.section, request.get_full_path())
    return course, curr_section


def student_page_start(request, course_id):
    try:
        course = CourseModel.objects.get(id=course_id)
    except CourseModel.DoesNotExist:
        raise Http404
    has_access = has_access_to_student_course(request.user, course)
    if not has_access:
        raise PermissionDenied
    curr_section = get_section_by_url(course.section, request.get_full_path())
    return course, curr_section


def generate_questions_list(test):
    test_questions = QuestionModel.objects.filter(test=test).order_by('id')

    no_groups_questions = []
    groups = {}
    for question in test_questions:
        question_groups = Question2Group.objects.filter(question=question).order_by('id').values_list('group',
                                                                                                      flat=True)
        for group in question_groups:
            if group == '':
                no_groups_questions.append(question)
            else:
                groups.setdefault(group, []).append(question)

        if question_groups.__len__() == 0:
            no_groups_questions.append(question)

    import random
    questions = []
    for key, value in groups.items():
        random.shuffle(value)
        questions.append(value)

    noq = test.number_of_questions
    # нок = группы - по одному, нок < групп - рандом группы = нок, по одному. нок = группы + 1
    random.shuffle(questions)
    random.shuffle(no_groups_questions)
    result = []

    if noq == 0 or noq == None:
        for question_list in questions:
            result.append(question_list.pop())
        result += no_groups_questions
    else:
        for question_list in questions:
            noq -= 1
            result.append(question_list.pop())
            if noq < 0:
                break
        while noq > 0:
            result.append(no_groups_questions.pop())
            noq -= 1
    return result


class DeleteCourseView(views.View):
    def post(self, request, id):
        try:
            course = CourseModel.objects.get(id=id)
        except:
            raise Http404
        if not has_admin_permission(request.user):
            raise Http404
        course.delete()
        return redirect('courses_app:courses')


class EmployeeSectionView(views.View):
    def get(self, request, course_id):
        course, curr_section = employee_page_start(request, course_id)
        sections = SectionModel.objects.filter(
            section_of_this_section__in=Section2Sections.objects.filter(section=curr_section)).order_by('id')
        tests = TestsModel.objects.filter(section=curr_section).order_by('id')
        context = {
            'sections': sections,
            'tests': tests,
            'course': course,
        }
        return render(request, 'courses/employee.html', context)


class EmployeeTestRateView(views.View):
    def get(self, request, course_id, id, user_id, try_id):
        course, curr_section = employee_page_start(request, course_id)

        test = TestsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        user = User.objects.get(id=user_id)
        try_entry = TriesModel.objects.filter(test=test, student=user).order_by('id')[int(try_id) - 1]
        answers = Try2Question.objects.filter(try_field=try_entry).order_by('id')

        automaticly_rated = []
        not_automaticly_rated = []
        rate_forms = []
        counter = 0
        for answer in answers:
            if answer.question.type == 'r' or answer.question.type == 'c':
                real_answers = CheckOrRadioAnswerModel.objects.filter(question=answer.question).order_by('id')
                import json
                try:
                    answer.answer = list(json.loads('{"ans": ' + answer.answer.replace("'", '"') + '}')['ans'])
                except:
                    answer.answer = None
                automaticly_rated.append({'answer': answer, 'real_answers': real_answers})
            else:
                rate_forms.append(EmployeeRateForm(prefix=counter, instance=answer))
                counter += 1
                not_automaticly_rated.append(answer)
        context = {
            'test': test,
            'user': user,
            'try': try_entry,
            'try_no': try_id,
            'automaticly_rated': automaticly_rated,
            'not_automaticly_rated': not_automaticly_rated,
            'rate_forms': rate_forms,
        }
        return render(request, 'courses/employee_rate.html', context)

    def post(self, request, course_id, id, user_id, try_id):
        course, curr_section = employee_page_start(request, course_id)

        test = TestsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        user = User.objects.get(id=user_id)
        try_entry = TriesModel.objects.filter(test=test, student=user).order_by('id')[int(try_id) - 1]
        answers = Try2Question.objects.filter(try_field=try_entry).order_by('id')
        counter = 0
        models = []
        for answer in answers:
            if answer.question.type == 'f' or answer.question.type == 'i':
                form = EmployeeRateForm(request.POST, prefix=counter, instance=answer)
                if not form.is_valid():
                    raise Http404
                models.append(form.save(commit=False))
                models[-1].rate = min(models[-1].rate, answer.question.rating)
                counter += 1

        for model in models:
            model.save()
        try_entry.rated = True
        rating, max_rating = get_try_rating(try_entry)
        try_entry.rating = rating
        try_entry.max_rating = max_rating
        try_entry.save()
        return redirect('../../../../')


class EmployeeTestView(views.View):
    def get(self, request, course_id, id):
        course, curr_section = employee_page_start(request, course_id)

        test = TestsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        test_questions = QuestionModel.objects.filter(test=test).order_by('id')
        users = User.objects.filter(triesmodel__test=test).order_by('id').distinct()

        users_tries = []
        for user in users:
            tries = TriesModel.objects.filter(student=user, test=test).order_by('id')
            users_tries.append({
                'user': user,
                'tries': tries,
            })

        type_from_val = {
            'r': 'Один вариант ответа',
            'c': 'Несколько вариантов ответа',
            'i': 'Свой ответ',
            'f': 'Прикрепление файла',
        }
        groups = {}
        for question in test_questions:
            question.type = type_from_val[question.type]
            question_groups = Question2Group.objects.filter(question=question).order_by('id').values_list('group',
                                                                                                          flat=True)
            for group in question_groups:
                groups.setdefault(group, []).append(question)

            if question_groups.__len__() == 0:
                groups.setdefault('', []).append(question)

        context = {
            'test': test,
            'groups': groups,
            'users_tries': users_tries,
        }
        return render(request, 'courses/employee_test.html', context)


class ShowResults(views.View):
    def get(self, request, course_id, id):
        return render(request, 'courses/results.html')


class CourseInfoView(views.View):
    def get(self, request, id):
        try:
            course = CourseModel.objects.get(id=id)
        except:
            raise Http404
        teachers = User.objects.filter(course2teacher__course=course).order_by('username')
        print(teachers)
        context = {
            'teachers': teachers,
        }
        return render(request, 'courses/info.html', context)


class StudentTestShowTryView(views.View):
    def get(self, request, course_id, id, try_id):
        course, curr_section = student_page_start(request, course_id)

        test = TestsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        user = request.user
        try_entry = TriesModel.objects.filter(test=test, student=user).order_by('id')[int(try_id) - 1]
        answers = Try2Question.objects.filter(try_field=try_entry).order_by('id')

        automaticly_rated = []
        not_automaticly_rated = []
        rate_forms = []
        counter = 0
        for answer in answers:
            if answer.question.type == 'r' or answer.question.type == 'c':
                real_answers = CheckOrRadioAnswerModel.objects.filter(question=answer.question).order_by('id')
                import json
                try:
                    answer.answer = list(json.loads('{"ans": ' + answer.answer.replace("'", '"') + '}')['ans'])
                except:
                    answer.answer = None
                automaticly_rated.append({'answer': answer, 'real_answers': real_answers})
            else:
                rate_forms.append(EmployeeRateForm(prefix=counter, instance=answer))
                counter += 1
                not_automaticly_rated.append(answer)
        context = {
            'test': test,
            'user': user,
            'try': try_entry,
            'try_no': try_id,
            'automaticly_rated': automaticly_rated,
            'not_automaticly_rated': not_automaticly_rated,
            'rate_forms': rate_forms,
        }
        return render(request, 'courses/student_test_show_try_view.html', context)

class StudentTestTryView(views.View):
    def get(self, request, course_id, id):
        course, curr_section = student_page_start(request, course_id)
        test = TestsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]

        import datetime
        tries = TriesModel.objects.filter(test=test, student=request.user).order_by('id')
        try_no = tries.count()
        if test.time_restriction != 0 \
                and test.time_restriction is not None \
                and tries.last() is not None \
                and datetime.datetime.utcnow() < (
                tries.last().date_started + datetime.timedelta(minutes=test.time_restriction + 0.1)).replace(tzinfo=None) \
                and tries.last().date_submitted is None:
            try_entry = tries.last()
            db_questions = Try2Question.objects.filter(try_field=try_entry).order_by('id')
            questions = QuestionModel.objects.filter(try2question__try_field__student=request.user, test=test)
        elif try_no == test.tries and test.tries != 0 and test.tries is not None:
            raise Http404
        else:
            try_entry = TriesModel(student=request.user, test=test)
            try_entry.date_started = datetime.datetime.utcnow()
            try_entry.save()
            try_no += 1
            questions = generate_questions_list(test)
            db_questions = []
            for question in questions:
                t2q = Try2Question(try_field=try_entry, question=question)
                db_questions.append(t2q)
                t2q.save()
        f_n_q = []
        # generate forms
        for index, question in enumerate(db_questions):
            type = question.question.type
            if type == 'r':
                f_n_q.append({
                    'form': UserQuestionRadioForm(instance=question, prefix=index),
                    'question': questions[index],
                })
                answers = []
                answrs = CheckOrRadioAnswerModel.objects.filter(question=question.question)
                for answer in answrs:
                    answers.append((answer.text, answer.text))
                f_n_q[-1]['form'].fields['answer'].choices = answers
            elif type == 'c':
                f_n_q.append({
                    'form': UserQuestionCheckForm(instance=question, prefix=index),
                    'question': questions[index],
                })
                answers = []
                answrs = CheckOrRadioAnswerModel.objects.filter(question=question.question)
                for answer in answrs:
                    answers.append((answer.text, answer.text))
                f_n_q[-1]['form'].fields['answer'].choices = answers
            elif type == 'i':
                f_n_q.append({
                    'form': UserQuestionInputForm(instance=question, prefix=index),
                    'question': questions[index],
                })
            else:
                f_n_q.append({
                    'form': UserQuestionFileForm(instance=question, prefix=index),
                    'question': questions[index],
                })
        time_left = None
        if test.time_restriction is not None and test.time_restriction != 0:
            time_left = (datetime.timedelta(minutes=test.time_restriction) + try_entry.date_started.replace(tzinfo=None) - datetime.datetime.utcnow())
            time_left = (time_left - datetime.timedelta(microseconds=time_left.microseconds)).total_seconds()
        context = {
            'test': test,
            'forms_and_questions': f_n_q,
            'questions': questions,
            'try_no': try_no,
            'time_left': time_left
        }
        return render(request, 'courses/student_try.html', context)

    def post(self, request, course_id, id):
        course, curr_section = student_page_start(request, course_id)
        test = TestsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]

        try_entry = TriesModel.objects.filter(student=request.user, test=test).order_by('date_started').last()
        questions = Try2Question.objects.filter(try_field=try_entry).order_by('id')

        forms = []
        for index, question in enumerate(questions):
            my_type = question.question.type
            if my_type == 'r':
                forms.append(UserQuestionRadioForm(request.POST, instance=question, prefix=index))
                answers = []
                answrs = CheckOrRadioAnswerModel.objects.filter(question=question.question)
                for answer in answrs:
                    answers.append((answer.text, answer.text))
                forms[-1].fields['answer'].choices = answers
            elif my_type == 'c':
                forms.append(UserQuestionCheckForm(request.POST, instance=question, prefix=index))
                answers = []
                answrs = CheckOrRadioAnswerModel.objects.filter(question=question.question)
                for answer in answrs:
                    answers.append((answer.text, answer.text))
                forms[-1].fields['answer'].choices = answers
            elif my_type == 'i':
                forms.append(UserQuestionInputForm(request.POST, instance=question, prefix=index))
            else:
                forms.append(UserQuestionFileForm(request.POST, request.FILES, instance=question, prefix=index))
        for form in forms:
            if not form.is_valid():
                raise Http404
        import datetime
        try_entry.date_submitted = datetime.datetime.utcnow()
        was_i_or_f = False
        for form in forms:
            mod = form.save(commit=False)
            my_type = mod.question.type
            if my_type == 'r' or my_type == 'c':
                rating = mod.question.rating
                correct_answers_count = CheckOrRadioAnswerModel.objects.filter(question=mod.question,
                                                                               is_correct=True).count()
                answer = mod.answer
                correct = 0
                model_answer = CheckOrRadioAnswerModel.objects.filter(question=mod.question)
                if type(answer) == str:
                    try:
                        print(answer)
                        import ast
                        parsed = ast.parse(answer, mode='eval')
                        fixed = ast.fix_missing_locations(parsed)
                        compiled = compile(fixed, '<string>', 'eval')
                        print(compiled)
                        answer = eval(compiled)
                    except:
                        answer = [answer]
                else:
                    try:
                        answer = list(answer)
                    except TypeError:
                        answer = [answer]
                for ans in answer:
                    for model_ans in model_answer:
                        if ans == model_ans.text and model_ans.is_correct:
                            correct += 1
                        elif ans == model_ans.text and not model_ans.is_correct:
                            correct -= 1
                if correct == 0:
                    rate = 0
                else:
                    rate = rating * (correct / max(1, correct_answers_count))
                mod.rate = rate
                mod.answer = answer
            else:
                was_i_or_f = True
            mod.save()
        if not was_i_or_f:
            try_entry.rated = True
            rating, max_rating = get_try_rating(try_entry)
            try_entry.rating = rating
            try_entry.max_rating = max_rating
        try_entry.save()
        return redirect('../')


class TeacherTestDeleteView(views.View):
    def post(self, request, course_id, id):
        course, curr_section = teacher_page_start(request, course_id)
        test = TestsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        test.delete()
        return redirect('../../..')


class EditCourseView(views.View):
    def get(self, request, id):
        try:
            course = CourseModel.objects.get(id=id)
        except:
            raise Http404
        if not has_admin_permission(request.user):
            raise Http404
        form = EditCourseForm(instance=course)
        context = {
            'form': form,
            'id': id,
        }
        return render(request, 'courses/edit.html', context)

    def post(self, request, id):
        try:
            course = CourseModel.objects.get(id=id)
        except:
            raise Http404
        if not has_admin_permission(request.user):
            raise Http404
        form = EditCourseForm(request.POST, instance=course)
        if form.is_valid():
            news = form.save()
        return redirect('courses_app:courses')


class TeacherSectionView(views.View):
    def get(self, request, course_id):
        course, curr_section = teacher_page_start(request, course_id)
        sections = SectionModel.objects.filter(
            section_of_this_section__in=Section2Sections.objects.filter(section=curr_section)).order_by('id')
        tests = TestsModel.objects.filter(section=curr_section).order_by('id')
        pages = PagesModel.objects.filter(section=curr_section).order_by('id')
        documents = DocumentsModel.objects.filter(section=curr_section).order_by('id')
        context = {
            'sections': sections,
            'pages': pages,
            'tests': tests,
            'documents': documents,
            'course': course,
        }
        return render(request, 'courses/teacher/index.html', context)


class StudentSectionView(views.View):
    def get(self, request, course_id):
        course, curr_section = student_page_start(request, course_id)
        sections = SectionModel.objects.filter(
            section_of_this_section__in=Section2Sections.objects.filter(section=curr_section)).order_by('id')
        tests = TestsModel.objects.filter(section=curr_section).order_by('id')
        pages = PagesModel.objects.filter(section=curr_section).order_by('id')
        documents = DocumentsModel.objects.filter(section=curr_section).order_by('id')
        max_rate_tries = []
        for test in tests:
            max_rate_tries.append(TriesModel.objects.filter(test=test).order_by('rating').last())
        print(max_rate_tries)
        context = {
            'sections': sections,
            'pages': pages,
            'tests': tests,
            'documents': documents,
            'course': course,
            'max_rate_tries': max_rate_tries,
        }
        return render(request, 'courses/student.html', context)


class TeacherSectionAddView(views.View):
    def get(self, request, course_id):
        course, curr_section = teacher_page_start(request, course_id)

        form = EditSectionForm()
        context = {
            'form': form,
        }
        return render(request, 'courses/teacher/add_section.html', context)

    def post(self, request, course_id):
        course, curr_section = teacher_page_start(request, course_id)

        form = EditSectionForm(request.POST)
        if form.is_valid():
            section = form.save()
            Section2Sections.objects.create(section=curr_section, sections=section)

        return redirect('..', course_id=course_id)


class StudentTestMainShowView(views.View):
    def get(self, request, course_id, id):
        course, curr_section = student_page_start(request, course_id)

        test = TestsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        test_questions = QuestionModel.objects.filter(test=test).order_by('id')
        tries = TriesModel.objects.filter(student=request.user, test=test).order_by('id')

        groups = set()
        without_groups_count = 0
        for question in test_questions:
            groups.union(
                Question2Group.objects.filter(question=question).order_by('id').values_list('group', flat=True))
            without_groups_count += 1

        if test.number_of_questions is None:
            question_count = without_groups_count + groups.__len__()
        else:
            question_count = min(without_groups_count + groups.__len__(), test.number_of_questions)
        import datetime
        no_test_button = False
        if test.time_restriction != 0 \
                and test.time_restriction is not None \
                and tries.last() is not None \
                and datetime.datetime.utcnow() < (
                tries.last().date_started + datetime.timedelta(minutes=test.time_restriction + 0.1)).replace(tzinfo=None) \
                and tries.last().date_submitted is None:
            pass
        elif tries.count() == test.tries and test.tries != 0 and test.tries is not None:
            no_test_button = True
        print(no_test_button)
        context = {
            'test': test,
            'question_count': question_count,
            'tries': tries,
            'no_test_button': no_test_button or None,
        }
        return render(request, 'courses/student_test_main.html', context)


class TeacherTestShowView(views.View):
    def get(self, request, course_id, id):
        course, curr_section = teacher_page_start(request, course_id)

        test = TestsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        test_questions = QuestionModel.objects.filter(test=test).order_by('id')

        type_from_val = {
            'r': 'Один вариант ответа',
            'c': 'Несколько вариантов ответа',
            'i': 'Свой ответ',
            'f': 'Прикрепление файла',
        }
        groups = {}
        for question in test_questions:
            question.type = type_from_val[question.type]
            question_groups = Question2Group.objects.filter(question=question).order_by('id').values_list('group',
                                                                                                          flat=True)
            for group in question_groups:
                groups.setdefault(group, []).append(question)

            if question_groups.__len__() == 0:
                groups.setdefault('', []).append(question)

        context = {
            'test': test,
            'groups': groups,
        }
        return render(request, 'courses/teacher/show_test.html', context)


class TeacherTestAddView(views.View):
    def get(self, request, course_id):
        course, curr_section = teacher_page_start(request, course_id)

        form = EditTestForm()
        context = {
            'form': form,
        }
        return render(request, 'courses/teacher/add_test.html', context)

    def post(self, request, course_id):
        course, curr_section = teacher_page_start(request, course_id)
        form = EditTestForm(request.POST)
        if form.is_valid():
            from json import loads
            my_json = loads(request.POST['my_json'])
            my_questions = my_json['questions']
            test = form.save(commit=False)
            question_forms = []
            answer_forms = []
            questions = []
            answers = []
            groups_list = []

            test = form.save(commit=False)
            test.section = curr_section
            for question in my_questions:
                question_forms.append(EditQuestionForm(data=question))
                if not question_forms[-1].is_valid():
                    raise Http404

                questions.append(question_forms[-1].save(commit=False))
                groups = question['groups']
                if groups is None:
                    groups = []
                if not isinstance(groups, list):
                    raise Http404
                groups_list.append({'groups': groups, 'question': questions[-1]})
                for answer in question['answers']:
                    answer_forms.append(EditAnswerForm(data=answer))
                    if not answer_forms[-1].is_valid():
                        raise Http404
                    answers.append({'answer': answer_forms[-1].save(commit=False), 'question': questions[-1]})
            if questions.__len__() == 0:
                raise Http404

            test.save()
            for question in questions:
                question.test = test
                question.save()
            for answer in answers:
                print(answer['answer'])
                answer['answer'].question = answer['question']
                answer['answer'].save()

            for group_entry in groups_list:
                for group in group_entry['groups']:
                    Question2Group.objects.create(question=group_entry['question'], group=group)

        return redirect('..', course_id=course_id)


class TeacherTestEditView(views.View):
    def get(self, request, course_id, id):
        course, curr_section = teacher_page_start(request, course_id)

        test = TestsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        form = EditTestForm(instance=test)

        my_questions = []
        questions = QuestionModel.objects.filter(test=test).order_by('id')
        for question in questions:
            groups = Question2Group.objects.filter(question=question).order_by('id').values_list('group', flat=True)
            my_questions.append({
                'type': question.type,
                'groups': list(groups),
                'question': question.question,
                'hint': question.hint,
                'rating': question.rating,
                'answers': [],
            })
            answers = CheckOrRadioAnswerModel.objects.filter(question=question).order_by('id')
            for answer in answers:
                my_questions[-1]['answers'].append({
                    'text': answer.text,
                    'is_correct': answer.is_correct,
                })
        import json
        my_questions = json.dumps(my_questions)
        context = {
            'form': form,
            'my_questions': my_questions,
        }
        return render(request, 'courses/teacher/edit_test.html', context)

    def post(self, request, course_id, id):
        course, curr_section = teacher_page_start(request, course_id)

        test = TestsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        form = EditTestForm(request.POST, instance=test)
        if form.is_valid():
            from json import loads
            my_json = loads(request.POST['my_json'])
            my_questions = my_json['questions']
            test = form.save(commit=False)
            question_forms = []
            answer_forms = []
            questions = []
            answers = []
            groups_list = []

            test.section = curr_section
            for question in my_questions:
                question_forms.append(EditQuestionForm(data=question))
                if not question_forms[-1].is_valid():
                    raise Http404

                questions.append(question_forms[-1].save(commit=False))
                groups = question['groups']
                if groups is None:
                    groups = []
                if not isinstance(groups, list):
                    raise Http404
                groups_list.append({'groups': groups, 'question': questions[-1]})
                for answer in question['answers']:
                    answer_forms.append(EditAnswerForm(data=answer))
                    if not answer_forms[-1].is_valid():
                        raise Http404
                    answers.append({'answer': answer_forms[-1].save(commit=False), 'question': questions[-1]})
            if questions.__len__() == 0:
                raise Http404
            QuestionModel.objects.filter(test=test).delete()
            test.save()
            for question in questions:
                CheckOrRadioAnswerModel.objects.filter(question=question).delete()
                Question2Group.objects.filter(question=question).delete()
                question.test = test
                question.save()
            for answer in answers:
                answer['answer'].question = answer['question']
                answer['answer'].save()

            for group_entry in groups_list:
                for group in group_entry['groups']:
                    Question2Group.objects.create(question=group_entry['question'], group=group)

        return redirect('..', course_id=course_id)


class TeacherSectionEditView(views.View):
    def get(self, request, course_id):
        course, curr_section = teacher_page_start(request, course_id)

        form = EditSectionForm(instance=curr_section)
        context = {
            'form': form,
        }
        return render(request, 'courses/teacher/edit_section.html', context)

    def post(self, request, course_id):
        course, curr_section = teacher_page_start(request, course_id)

        form = EditSectionForm(request.POST, instance=curr_section)
        if form.is_valid():
            section = form.save()

        return redirect('..', course_id=course_id)


class TeacherSectionDeleteView(views.View):
    def post(self, request, course_id):
        course, curr_section = teacher_page_start(request, course_id)

        curr_section.delete()
        return redirect('../..')


class TeacherPageAddView(views.View):
    def get(self, request, course_id):
        course, curr_section = teacher_page_start(request, course_id)

        form = EditPageForm()
        context = {
            'form': form,
        }
        return render(request, 'courses/teacher/add_page.html', context)

    def post(self, request, course_id):
        course, curr_section = teacher_page_start(request, course_id)

        form = EditPageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.section = curr_section
            page.save()

        return redirect('..', course_id=course_id)


class TeacherDocumentAddView(views.View):
    def get(self, request, course_id):
        course, curr_section = teacher_page_start(request, course_id)

        form = EditDocumentForm()
        context = {
            'form': form,
        }
        return render(request, 'courses/teacher/add_document.html', context)

    def post(self, request, course_id):
        course, curr_section = teacher_page_start(request, course_id)

        form = EditDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.section = curr_section
            document.save()

        return redirect('..', course_id=course_id)


class TeacherPageEditView(views.View):
    def get(self, request, course_id, id):
        course, curr_section = teacher_page_start(request, course_id)
        page = PagesModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        form = EditPageForm(instance=page)
        context = {
            'form': form,
        }
        return render(request, 'courses/teacher/edit_page.html', context)

    def post(self, request, course_id, id):
        course, curr_section = teacher_page_start(request, course_id)

        page = PagesModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        form = EditPageForm(request.POST, instance=page)
        if form.is_valid():
            page = form.save()

        return redirect('..', course_id=course_id)


class TeacherDocumentEditView(views.View):
    def get(self, request, course_id, id):
        course, curr_section = teacher_page_start(request, course_id)

        document = DocumentsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        form = EditDocumentForm(instance=document)
        context = {
            'form': form,
        }
        return render(request, 'courses/teacher/edit_document.html', context)

    def post(self, request, course_id, id):
        course, curr_section = teacher_page_start(request, course_id)

        document = DocumentsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        form = EditDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            document = form.save()

        return redirect('..', course_id=course_id)


class TeacherPageDeleteView(views.View):
    def post(self, request, course_id, id):
        course, curr_section = teacher_page_start(request, course_id)
        page = PagesModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        page.delete()
        return redirect('../../..')


class TeacherDocumentDeleteView(views.View):
    def post(self, request, course_id, id):
        course, curr_section = teacher_page_start(request, course_id)

        document = DocumentsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        document.delete()
        return redirect('../../..')


class PageShowView(views.View):
    def get(self, request, course_id, id):
        course, curr_section = student_page_start(request, course_id)
        page = PagesModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        context = {
            'name': page.name,
            'content': page.content,
        }
        return render(request, 'courses/page.html', context)


class DocumentShowView(views.View):
    def get(self, request, course_id, id):
        course, curr_section = student_page_start(request, course_id)
        document = DocumentsModel.objects.filter(section=curr_section).order_by('id')[int(id) - 1]
        return redirect(document.document.url)


class MainCoursesView(views.View):
    def get(self, request):
        has_admin_perm = has_admin_permission(request.user)
        student_courses = None
        employee_courses = None
        teacher_courses = None
        if has_admin_perm:
            student_courses = CourseModel.objects.all().order_by('id')
            employee_courses = CourseModel.objects.all().order_by('id')
            teacher_courses = CourseModel.objects.all().order_by('id')
        elif request.user.is_authenticated:
            student_courses = CourseModel.objects.filter(
                course2student__in=Course2Student.objects.filter(student=request.user)).order_by('id')
            employee_courses = CourseModel.objects.filter(
                course2employee__in=Course2Employee.objects.filter(employee=request.user)).order_by('id')
            teacher_courses = CourseModel.objects.filter(
                course2teacher__in=Course2Teacher.objects.filter(teacher=request.user)).order_by('id')
        context = {
            'student_courses': student_courses,
            'employee_courses': employee_courses,
            'teacher_courses': teacher_courses,
            'has_permission_to_add': has_admin_perm
        }
        return render(request, 'courses/index.html', context)


class AddCourseView(views.View):
    def get(self, request):
        if not has_admin_permission(request.user):
            raise Http404
        form = EditCourseForm()
        context = {
            'form': form,
        }
        return render(request, 'courses/add.html', context)

    def post(self, request):
        if not has_admin_permission(request.user):
            raise Http404

        form = EditCourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.section = SectionModel.objects.create()
            course.save()
            return redirect('courses_app:courses')
        else:
            return redirect('courses_app:add_course')
