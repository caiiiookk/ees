from .models import Section2Sections, SectionModel, CourseModel, PagesModel
from django.urls import reverse

def path_widget(request):
    # names = {
    #     'courses': 'Курсы',
    #     't-course': 'Преподавательский курс',
    #     'section': 'Раздел',
    #     'page': 'Страница',
    #     'edit': 'Изменение',
    #     'delete': 'Удаление',
    #     's-course': 'Студенческий курс',
    # }
    # if request.resolver_match.app_name != 'courses_app':
    #     return ''
    # full_path = request.get_full_path()
    # splitted = str(full_path).split('/')[1:]
    # if splitted.__len__() < 3:
    #     return ''
    # splitted = splitted[1:]
    # while splitted[-1] == '':
    #     splitted = splitted[:-1]
    # url_sections = splitted[0::2]
    # ids = splitted[1::2]
    # result = '<a href="' + reverse('courses_app:courses') + '" class="header_path">Курсы</a>&nbsp;&gt;&nbsp;'
    # tmp_counter = 0
    # print(url_sections)
    # for index, elem in enumerate(url_sections):
    #     if elem == 'section':
    #         last_section = SectionModel.objects.filter(section_of_this_section__in=Section2Sections.objects.filter(section=last_section))[int(ids[index]) - 1]
    #         name = last_section.name
    #     elif elem == 't-course' or elem == 'e-course' or elem == 'o-course' or elem == 's-course':
    #         course = CourseModel.objects.get(id=ids[index])
    #         name = course.name
    #         last_section = course.section
    #     elif elem == 'page':
    #         name = PagesModel.objects.get(id=ids[index - 1]).name
    #     elif elem == 'edit':
    #         pass
    #     else:
    #         continue
    #     result += '<a href="' + ''.join(['../' for x in range((ids.__len__() - index - 1) * 2)]) + '" class="header_path">' + name + ' (' + str(names[elem]) + ')</a>&nbsp;&gt;&nbsp;'
    return {'path_widget': ''}
