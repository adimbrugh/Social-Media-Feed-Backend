from .queries import InteractionQueries
from .mutations import InteractionMutations
import graphene



class InteractionSchema(InteractionQueries, InteractionMutations, graphene.ObjectType):
    pass

