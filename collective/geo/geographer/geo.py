from Acquisition import aq_base
from zope.interface import implements
from zope.component import adapts
from zope.event import notify
from zope.annotation.interfaces import IAnnotations
from persistent.dict import PersistentDict
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.geographer.interfaces import IWriteGeoreferenced
from collective.geo.geographer.event import ObjectGeoreferencedEvent

import logging

logger = logging.getLogger('collective.geo.geographer')

KEY = 'collective.geo.geographer.georeference'


class GeoreferencingAnnotator(object):
    """Geographically annotate objects with metadata modeled after GeoJSON.
    See http://geojson.org
    """
    implements(IWriteGeoreferenced)
    adapts(IGeoreferenceable)

    def __init__(self, context):
        self.context = aq_base(context)
        annotations = IAnnotations(self.context)
        self.geo = annotations.get(KEY, None)
        if not self.geo:
            annotations[KEY] = PersistentDict()
            self.geo = annotations[KEY]
            self.geo['type'] = None
            self.geo['coordinates'] = None
            self.geo['crs'] = None

    @property
    def type(self):
        return self.geo['type']

    @property
    def coordinates(self):
        return self.geo['coordinates']

    @property
    def crs(self):
        return self.geo['crs']

    def setGeoInterface(self, type, coordinates, crs=None):
        self.geo['type'] = type
        self.geo['coordinates'] = coordinates
        self.geo['crs'] = crs
        # commented out since it breaks collective.geo.behaviour:
        # http://plone.293351.n2.nabble.com/collective-geo-behaviour-td7127292.html
        #notify(ObjectGeoreferencedEvent(self.context))

    def removeGeoInterface(self):
        attrs = ['type', 'coordinates', 'crs']
        for key in attrs:
            self.geo[key] = None
        notify(ObjectGeoreferencedEvent(self.context))
