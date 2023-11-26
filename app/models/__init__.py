import rdflib

rdflib.plugin.register("turtle_custom", rdflib.plugin.Serializer, "app.models.serializer", "TurtleSerializerCustom")
