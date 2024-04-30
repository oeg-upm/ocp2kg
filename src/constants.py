import logging, coloredlogs

##############################################################################
#############################   RML CONSTANTS  ###############################
##############################################################################

RML_URI = 'http://semweb.mmlab.be/ns/rml#'
R2RML_URI = 'http://www.w3.org/ns/r2rml#'
RDF_URI = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
D2RQ_URI = 'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#'
QL_URI = 'http://semweb.mmlab.be/ns/ql#'
EXAMPLE_URI = 'http://example.com/ns#'
RDFS_URI = 'http://www.w3.org/2000/01/rdf-schema#'
XSD_URI = 'http://www.w3.org/2001/XMLSchema#'
FOAF_URI = 'http://xmlns.com/foaf/0.1/'
RDF_TYPE = 'rdf:type'
SCHEMA_URI = 'http://schema.org/'
STAR_URI = 'https://w3id.org/kg-construct/rml-star'
COMPRESSION_URI = 'http://semweb.mmlab.be/ns/rml-compression#'
FORMATS_URI = 'http://www.w3.org/ns/formats/'
VOID_URI = 'http://rdfs.org/ns/void#'
FNML_URI = 'http://semweb.mmlab.be/ns/fnml#'
GREL_URI = 'http://users.ugent.be/~bjdmeest/function/grel.ttl#'

R2RML_PREFIX = 'rr'
RML_PREFIX = 'rml'

TURTLE_PREFIX = '@prefix'
RML_BASE = '@base'
RML_LOGICAL_SOURCE_CLASS = f'{RML_PREFIX}:LogicalSource'
RML_LOGICAL_SOURCE = f'{RML_PREFIX}:logicalSource'
RML_SOURCE = f'{RML_PREFIX}:source'
RML_REFERENCE_FORMULATION = f'{RML_PREFIX}:referenceFormulation'
RML_ITERATOR = f'{RML_PREFIX}:iterator'
RML_REFERENCE = f'{RML_PREFIX}:reference'
RML_LANGUAGE_MAP = f'{RML_PREFIX}:languageMap'
RML_LANGUAGE_MAP_CLASS = f'{RML_PREFIX}:LanguageMap'
RML_DATATYPE_MAP = f'{RML_PREFIX}:datatypeMap'
RML_DATATYPE_MAP_CLASS = f'{RML_PREFIX}:DatatypeMap'
RML_QUERY = f'{RML_PREFIX}:query'

RML_LOGICAL_TARGET = f'{RML_PREFIX}:logicalTarget'
RML_LOGICAL_TARGET_CLASS = f'{RML_PREFIX}:LogicalTarget'
RML_TARGET = f'{RML_PREFIX}:target'
RML_SERIALIZATION = f'{RML_PREFIX}:serialization'
RML_COMPRESSION = f'{RML_PREFIX}:compression'

R2RML_TEMPLATE = f'{R2RML_PREFIX}:template'
R2RML_TRIPLES_MAP = f'{R2RML_PREFIX}:TriplesMap'
R2RML_CONSTANT = f'{R2RML_PREFIX}:constant'
R2RML_SUBJECT = f'{R2RML_PREFIX}:subjectMap'
R2RML_SUBJECT_CLASS = f'{R2RML_PREFIX}:SubjectMap'
R2RML_CLASS = f'{R2RML_PREFIX}:class'
R2RML_SQL_VERSION = f'{R2RML_PREFIX}:sqlVersion'
R2RML_SQL_QUERY = f'{R2RML_PREFIX}:sqlQuery'
R2RML_PREDICATE_OBJECT_MAP = f'{R2RML_PREFIX}:predicateObjectMap'
R2RML_PREDICATE_OBJECT_MAP_CLASS = f'{R2RML_PREFIX}:PredicateObjectMap'
R2RML_SHORTCUT_PREDICATE = f'{R2RML_PREFIX}:predicate'
R2RML_PREDICATE = f'{R2RML_PREFIX}:predicateMap'
R2RML_PREDICATE_CLASS = f'{R2RML_PREFIX}:PredicateMap'
R2RML_SHORTCUT_OBJECT = f'{R2RML_PREFIX}:object'
R2RML_OBJECT = f'{R2RML_PREFIX}:objectMap'
R2RML_OBJECT_CLASS = f'{R2RML_PREFIX}:ObjectMap'
R2RML_GRAPH = f'{R2RML_PREFIX}:graph'
R2RML_GRAPH_MAP = f'{R2RML_PREFIX}:graphMap'
R2RML_GRAPH_CLASS = f'{R2RML_PREFIX}:GraphMap'
R2RML_DATATYPE = f'{R2RML_PREFIX}:datatype'
R2RML_TERMTYPE = f'{R2RML_PREFIX}:termType'
R2RML_LANGUAGE = f'{R2RML_PREFIX}:language'
R2RML_IRI = f'{R2RML_PREFIX}:IRI'
R2RML_BLANK_NODE = f'{R2RML_PREFIX}:BlankNode'
R2RML_LITERAL = f'{R2RML_PREFIX}:Literal'
R2RML_REFOBJECT_CLASS = f'{R2RML_PREFIX}:RefObjectMap'
R2RML_PARENT_TRIPLESMAP = f'{R2RML_PREFIX}:parentTriplesMap'
R2RML_JOIN_CONITION = f'{R2RML_PREFIX}:joinCondition'
R2RML_CHILD = f'{R2RML_PREFIX}:child'
R2RML_PARENT = f'{R2RML_PREFIX}:parent'
R2RML_LOGICAL_TABLE_CLASS = f'{R2RML_PREFIX}:LogicalTable'
R2RML_LOGICAL_TABLE = f'{R2RML_PREFIX}:logicalTable'
R2RML_TABLE_NAME = f'{R2RML_PREFIX}:tableName'
R2RML_COLUMN = f'{R2RML_PREFIX}:column'

##############################################################################
#############################   D2RQ CONSTANTS  ##############################
##############################################################################
D2RQ_DATABASE_CLASS = 'd2rq:Database'
D2RQ_DSN = 'd2rq:jdbcDSN'
D2RQ_DRIVER = 'd2rq:jdbcDriver'
D2RQ_USER = 'd2rq:username'
D2RQ_PASS = 'd2rq:password'

##############################################################################
#############################  OCH CONSTANTS  ###############################
##############################################################################
# THIS NEEDS TO CHANGE TO OCH once we recreate all change KGs
OMV_ADDEDCLASS = 'omv:addedClass'

OMV_ADD_SUBCLASS_SUBJECT = 'omv:subAddSubClass'
OMV_ADD_SUBCLASS_OBJECT = 'omv:objAddSubClass'

##############################################################################
#############################  RDFS&OWL CONSTANTS  ###############################
##############################################################################

OWL_DATA_PROPERTY = 'owl:DatatypeProperty'
OWL_OBJECT_PROPERTY = 'owl:ObjectProperty'
RDFS_DOMAIN = 'rdfs:domain'
RDFS_RANGE = 'rdfs:range'

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', fmt='%(asctime)s,%(msecs)03d | %(levelname)s: %(message)s')
