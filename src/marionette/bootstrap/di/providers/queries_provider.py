from dishka.entities.scope import Scope
from dishka.provider.make_factory import provide
from dishka.provider.provider import Provider

from marionette.application.queries.characters import CharacterQueries


class QueryProvider(Provider):
    scope = Scope.REQUEST

    characters_query = provide(CharacterQueries)
