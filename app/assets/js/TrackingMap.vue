<template>
    <div id="container">
        <div id="mymap"></div>
        <img src="/static/us.png" id="logo">
        <div id="details" v-if="showHeading || showSpeed">
            <template v-if="showHeading">
                <small>Heading</small>
                <div>{{ direction }}</div>
                <small class="text-white">{{ currentDatapoint.heading }}°</small>
            </template>
            <hr v-if="showHeading && showSpeed">
            <template v-if="showSpeed">
                <small>Speed</small>
                <div>{{ currentDatapoint.ground_speed }}</div>
                <small class="text-white">km/h</small>
            </template>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    @mixin phone {
        @media (max-width: 720px) {
            @content;
        }
    }

    #container {
        height: 100%;

        #mymap {
            z-index: 1; height: 100%;

            @include phone {
                .leaflet-container .leaflet-control-attribution {
                    display: none !important;
                }
            }
        }

        #logo {
            position: absolute; 
            bottom: 0; left: 0; 
            z-index: 101; 
            max-width: 200px;

            @include phone {
                max-width: 150px;
                height: auto;
            }
        }

        .text-white { color: #fff !important; }

        #details {
            position: absolute; 
            top: 20px; right: 20px; 
            z-index: 101;
            background: rgba(0,0,0,0.7); 
            color: #fff;
            text-align: center;
            font-family: sans-serif;
            font-weight: bold;
            font-size: 1.2rem;
            padding: 1rem;
            border-radius: .5rem;

            small {
                font-size: .8rem;
                color: #999;
                text-transform: uppercase;
            }
        }
    }
</style>

<script>
    import axios from 'axios'
    import 'leaflet/dist/leaflet.css'
    import { map, tileLayer, marker, icon } from 'leaflet'

    let myMap
    let watcher
    let mapMarker
    const eastIcon = icon({
        iconUrl: '/static/marker_east.png',
        //iconSize: [128, 128],
        //iconAnchor: [20, 90],
        iconSize: [64, 64],
        iconAnchor: [10, 45],
        popupAnchor: [-3, -76],
        //shadowUrl: 'my-icon-shadow.png',
        //shadowSize: [68, 95],
        //shadowAnchor: [22, 94]
    })
    const westIcon = icon({
        iconUrl: '/static/marker_west.png',
        //iconSize: [128, 128],
        //iconAnchor: [20, 90],
        iconSize: [64, 64],
        iconAnchor: [10, 45],
        popupAnchor: [-3, -76],
        //shadowUrl: 'my-icon-shadow.png',
        //shadowSize: [68, 95],
        //shadowAnchor: [22, 94]
    })

    export default {
        data() {
            return {
                datapoints: [],
                currentDatapoint: null
            }
        },
        created() {
            this.watchPosition()
        },
        mounted() {
            myMap = map('mymap')

            tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
                id: 'mapbox/streets-v11',
                tileSize: 512,
                zoomOffset: -1,
                accessToken: 'pk.eyJ1IjoiZ3JlZW4yZ28iLCJhIjoiY2tkZXkzZG4zMm0ycDJ3c2NvcXN6Mm5wOCJ9.dZTIjRsPq7u-1g4f3Dtnkg'
            }).addTo(myMap);
        },
        methods: {
            watchPosition() {
                clearInterval(watcher)
                this.updatePosition().then(() => {
                    myMap.setView([
                        this.currentDatapoint.latitude, 
                        this.currentDatapoint.longitude
                    ], 14)
                })
                watcher = setInterval(this.updatePosition, 10000)
            },
            updatePosition() {
                return new Promise((resolve, reject) => {
                    axios.get('/data/current').then(r => {
                        this.currentDatapoint = r.data

                        if (!mapMarker) {
                            mapMarker = marker([
                                this.currentDatapoint.latitude, 
                                this.currentDatapoint.longitude
                            ], { icon: this.currentIcon }).addTo(myMap);
                        }

                        mapMarker.setIcon(this.currentIcon)

                        mapMarker.setLatLng([
                            this.currentDatapoint.latitude, 
                            this.currentDatapoint.longitude
                        ])

                        resolve()
                    }).catch(reject)
                })
            }
        },
        computed: {
            currentIcon() {
                if (!this.currentDatapoint)
                    return eastIcon

                let heading = this.currentDatapoint.heading

                if (heading > 0 && heading <= 180) {
                    return eastIcon
                }

                return westIcon
            },
            showHeading() {
                return this.currentDatapoint && this.currentDatapoint.heading
            },
            showSpeed() {
                return this.currentDatapoint && this.currentDatapoint.ground_speed
            },
            direction() {
                let heading = this.currentDatapoint.heading

                if (heading) {
                    if (heading >= 33.75 && heading < 78.75) {
                        return 'NE'
                    } else if (heading >= 78.75 && heading < 123.75) {
                        return 'E'
                    } else if (heading >= 123.75 && heading < 168.7) {
                        return 'SE'
                    } else if (heading >= 168.7 && heading < 213.75) {
                        return 'S'
                    } else if (heading >= 213.75 && heading < 258.75) {
                        return 'SW'
                    } else if (heading >= 258.75 && heading < 303.75) {
                        return 'W'
                    } else if (heading >= 303.75 && heading < 348.75) {
                        return 'NW'
                    } 
                    
                    return 'N'
                }
            }
        }
    }
</script>