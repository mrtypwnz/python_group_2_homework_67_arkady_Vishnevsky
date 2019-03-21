from webapp.models import Movie, Category, Hall, Seat, Show, Discount, Book, Ticket
from rest_framework import viewsets
from api_v1.serializers import MovieCreateSerializer, MovieDisplaySerializer, \
    CategorySerializer, HallSerializer, SeatSerializer, ShowSerializer, DiscountSerializer, BookSerializer, TicketSerializer
from rest_framework.permissions import IsAuthenticated


class BaseViewSet(viewsets.ModelViewSet):
    # Метод, который отвечает за проверку разрешений на доступ к данному ViewSet
    def get_permissions(self):
        permissions = super().get_permissions()
        # IsAuthenticated - класс разрешения, требующий аутентификацию
        # добавляем его объект ( IsAuthenticated() ) к разрешениям только
        # для "опасных" методов - добавление, редактирование, удаление данных.
        if self.request.method in ["POST", "DELETE", "PUT", "PATCH"]:
            permissions.append(IsAuthenticated())
        return permissions


class MovieViewSet(BaseViewSet):
    queryset = Movie.objects.active().order_by('id')

    # если в настройках REST_FRAMEWORK прописан django_filters в DEFAULT_FILTER_BACKENDS
    # то для базовых фильтров по полям модели достаточно указать это поле в ViewSet'е,
    # в котором перечислить список полей, по которым можно фильтровать.
    # filterset_fields = ('release_date',)

    # Метод, который отвечает за то,
    # какой класс сериализатора будет использоваться при обработке запроса.
    # Если запрос сделан методом GET, т.е. запрос на просмотр фильма или списка фильмов,
    # то метод возвращает класс MovieDisplaySerializer (вывод фильмов с вложенными категориями),
    # иначе - MovieCreateSerializer (вывод и сохранение фильмов с категориями в виде списка id категорий).
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MovieDisplaySerializer
        else:
            return MovieCreateSerializer

    # метод, который выполняет удаление объекта instance.
    # здесь он переопределён для "мягкого" удаления объектов -
    # вместо реального удаления объекта, меняется его свойство is_deleted на True.
    # сам фильм сохраняется в базе, но при этом помечается, как удалённый.
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    # вариант фильтрации без использования сторонних библиотек.
    # переопределяем метод get_queryset, и фильтруем в нём набор данных по параметрам запроса.

    # этот метод приведён для примера (для текущих задач он здесь не требуется).
    # def get_queryset(self):
    #     queryset = self.queryset
    #     release_date = self.request.query_params.get('release_date', None)
    #     if release_date is not None:
    #         queryset = queryset.filter(release_date__gte=release_date).order_by('-release_date')
    #     return queryset


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class HallViewSet(BaseViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer


class SeatViewSet(BaseViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class ShowViewSet(BaseViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

    # фильтр сеансов показа фильмов по id фильма и по дате начала сеанса
    # сюда требуется добавить фильтр по id зала.
    def get_queryset(self):
        queryset = Show.objects.all()
        movie_id = self.request.query_params.get('movie_id', None)
        hall_id = self.request.query_params.get('hall_id', None)
        starts_after = self.request.query_params.get('starts_after', None)
        starts_before = self.request.query_params.get('starts_before', None)

        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)
        if hall_id:
            queryset = queryset.filter(hall_id=hall_id)
        if starts_after:
            queryset = queryset.filter(starts_at__gte=starts_after)
        if starts_before:
            queryset = queryset.filter(starts_at__lte=starts_before)
        return queryset

class BookViewSet(BaseViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class TicketViewSet(BaseViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class DiscountViewSet(BaseViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer