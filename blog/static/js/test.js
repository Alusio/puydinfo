(function ($, Drupal) {
    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)), sURLVariables = sPageURL.split('&'),
            sParameterName, i;
        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] === sParam) return sParameterName[1] === undefined ? true : sParameterName[1]
        }
    }, OpenLayerPuyDuFou = function () {
        var layers = [], iconFeatures = [], centerPoint = [-0.9291, 46.8886], zone = [-0.92, 46.8852, -0.934, 46.8945],
            projectionIdFrom = 'EPSG:4326', projectionIdTo = 'EPSG:3857', map = null, current_feature = null;
        this.setOSMTileLayer = function () {
        };
        this.setPDFTileLayer = function () {
            var url = 'https://apps.api.puydufou.fr/tiles/tiles.php?z={z}&x={x}&y={-y}';
            this.setTileLayer(url)
        };
        this.setTileLayer = function (url) {
            var layer = new ol.layer.Tile({source: new ol.source.XYZ({url: url})});
            layers.push(layer)
        };
        this.buildMap = function (id) {
            var map = new ol.Map({
                target: id,
                layers: layers,
                view: new ol.View({
                    center: ol.proj.transform(centerPoint, projectionIdFrom, projectionIdTo),
                    zoom: 17,
                    maxZoom: 19,
                    minZoom: 16,
                    extent: ol.proj.transformExtent(zone, projectionIdFrom, projectionIdTo)
                })
            });
            this.map = map;
            this.selectInteraction = new ol.interaction.Select()
        };
        this.setMarkerStyle = function (iconFeature, icon_url) {
            if (icon_url === '' || icon_url === undefined) icon_url = 'https://openlayers.org/en/v4.6.4/examples/data/dot.png';
            var iconStyle = new ol.style.Style({
                image: new ol.style.Icon({
                    anchor: [0.5, 1],
                    anchorXUnits: 'fraction',
                    anchorYUnits: 'fraction',
                    crossOrigin: 'anonymous',
                    size: [120, 120],
                    scale: 0.5,
                    src: icon_url
                })
            });
            iconFeature.setStyle(iconStyle)
        };
        this.setDefaultMarker = function () {
            this.selectInteraction.getFeatures().clear();
            if (this.default_layer != null) {
                this.selectInteraction.getFeatures().push(this.default_layer);
                this.map.getView().setCenter(this.default_layer.getGeometry().getCoordinates())
            }
            ;this.map.addInteraction(this.selectInteraction)
        };
        this.setMarkers = function (items, type) {
            var olpdf = this, type_label = '';
            iconFeatures = [];
            var default_entity_open = getUrlParameter('entity');
            $.each(items, function (index, item) {
                if (type_label.length < 1) type_label = item.type_name;
                var iconFeature = new ol.Feature({
                    geometry: new ol.geom.Point(ol.proj.transform([parseFloat(item.lng), parseFloat(item.lat)], projectionIdFrom, projectionIdTo)),
                    title: item.title,
                    id: item.nid,
                    type: type,
                    lat: item.lat,
                    code: item.code,
                    url_entity: item.url_entity,
                    lng: item.lng,
                    url_icn_close: item.picto_close,
                    url_icn_open: item.picto_open
                });
                olpdf.setMarkerStyle(iconFeature, item.picto_close);
                iconFeatures.push(iconFeature);
                if (item.nid == default_entity_open) olpdf.default_layer = iconFeature
            });
            var vectorSource = new ol.source.Vector({features: iconFeatures});
            vectorLayer = new ol.layer.Vector({source: vectorSource});
            layers.push(vectorLayer);
            $('#filters .vector-types').append('<div class="filter" data-filter-type="' + type + '">' + type_label + '</div>');
            $('#filters .vector-types .filter').unbind();
            $('#filters .vector-types .filter').bind('click', function () {
                var type = $(this).attr('data-filter-type'), filter = $(this);
                $.each(layers, function (index, layer) {
                    var source = layer.getSource();
                    if (source.getProjection() !== null) return true;
                    var this_layer = false, features = source.getFeatures();
                    $.each(features, function (index_item, item_source) {
                        if (item_source.get('type') !== type) return false;
                        this_layer = true;
                        return false
                    });
                    if (this_layer) {
                        var visible = layer.getVisible();
                        if (visible) {
                            $(filter).addClass('disabled')
                        } else $(filter).removeClass('disabled');
                        layer.setVisible(!visible)
                    }
                })
            })
        };
        this.setPopup = function (id) {
            var olpdf = this, element = document.getElementById(id),
                popup = new ol.Overlay({element: element, positioning: 'bottom-center', stopEvent: false});
            this.map.addOverlay(popup);
            this.selectInteraction.getFeatures().on("add", function (e) {
                var feature = e.element;
                if (this.current_feature) {
                    olpdf.setMarkerStyle(this.current_feature, this.current_feature.get('url_icn_close'));
                    this.current_feature = null
                }
                ;
                if (feature) {
                    olpdf.setMarkerStyle(feature, feature.get('url_icn_open'));
                    var coordinates = feature.getGeometry().getCoordinates();
                    popup.setPosition(coordinates);
                    $(element).html("<div class='content'><span class='code element-" + feature.get('type') + "'>" + feature.get('code') + "</span><h2 style='white-space: nowrap;'><a href='" + feature.get('url_entity') + "' target='_blank'>" + feature.get('title') + "</a></h2>");
                    this.current_feature = feature;
                    return true
                }
                ;$(element).popover('hide')
            })
        }
    };
    Drupal.behaviors.mapcustom = {
        attach: function (context, settings) {
            if ($('#map .ol-viewport').length > 0) return;
            var map = new OpenLayerPuyDuFou();
            map.setOSMTileLayer();
            map.setPDFTileLayer();
            map.setMarkers(settings.pdf_map.show.items, 'show');
            map.setMarkers(settings.pdf_map.hotel.items, 'hotel');
            map.setMarkers(settings.pdf_map.restaurant.items, 'restaurant');
            map.buildMap('map');
            map.setPopup('popup-map');
            map.setDefaultMarker();
            $('#filters .vector-types .filter').eq(1).trigger('click');
            $('#filters .vector-types .filter').eq(2).trigger('click')
        }
    }
})(jQuery, Drupal)