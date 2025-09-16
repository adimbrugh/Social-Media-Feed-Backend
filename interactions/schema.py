import graphene
from .queries import InteractionQueries
from .mutations import InteractionMutations



class InteractionSchema(InteractionQueries, InteractionMutations, graphene.ObjectType):
    pass
