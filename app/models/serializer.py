from rdflib.plugins.serializers.turtle import TurtleSerializer


class TurtleSerializerCustom(TurtleSerializer):
    def getQName(self, uri, gen_prefix=True):
        return None
