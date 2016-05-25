from jinja2 import Template
from jinja2.ext import loopcontrols
import yaml

LAYERS_TO_BE_DOCUMENTED = [
    'adminarea_a',
    'building_a',
    'geoname_p',
    'landuse_a',
    'military_p',
    'misc_l',
    'natural_a',
    'nonop_l',
    'poi_p',
    'pow_p',
    'railway_bridge_l',
    'road_ground_l',
    'route_l',
    'traffic_a',
    'traffic_p',
    'transport_a',
    'utility_a',
    'utility_p',
    'utility_l',
    'water_a',
    'water_p',
    'water_l',
]

with open('templates/layer_attributes.md.jinja2') as f:
    LAYER_ATTRIBUTES_TEMPLATE = Template(f.read())
with open('templates/attribute_values.md.jinja2') as f:
    ATTRIBUTE_VALUES_TEMPLATE = Template(f.read())

#TODO osm_tags more than one
def yaml_to_md(layer_name, layer_definition, out):
    out.write('## ' + layer_name + '\n\n')

    attributes = layer_definition['attributes']
    header = "|Attributes          |type                |Description                                                           |osm_tags            |"
    header += "\n| ------------------ | ------------------ | -------------------------------------------------------------------- | ------------------ |"

    out.write(LAYER_ATTRIBUTES_TEMPLATE.render(attributes=attributes, header=header, dicts_len=len(attributes.keys())))

    # values of layer attribute "type" (not to be confused with an attribute's type)

    type_values = attributes["type"]['values']
    # osm_tags = attributes["type"]['values'][attributes["type"]['values']]['osm_tags']
    # tags_len = len(osm_tags.keys())
    
    correlated_attributes = set()
    for definition in type_values.values():
        for name, _ in definition.get('correlated_attributes', {}).items():
        	correlated_attributes.add(name)

    out.write(ATTRIBUTE_VALUES_TEMPLATE.render(type_values=type_values, correlated_attributes=correlated_attributes))
    out.write('\n\n')


with open("osmaxx_schema.yaml", 'r') as in_file:
    data = yaml.load(in_file)
layers = data['layers']
with open("documentation.md", 'w') as out_file:
    for layer_name in LAYERS_TO_BE_DOCUMENTED:
        yaml_to_md(layer_name, layers[layer_name], out=out_file)

'''
{%- if definition['osm_tags'][1] is defined -%}
        {{- definition['osm_tags'][1].keys()[0] }}='{{ definition['osm_tags'][1].values()[0] }}'|
    {%- else -%}
        |
    {%- endif -%}
'''