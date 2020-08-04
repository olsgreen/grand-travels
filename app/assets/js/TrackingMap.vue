<template>
    <div id="container">
        <div id="mymap"></div>
        <img src="/static/us.png" id="logo">
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
                left: auto;
                bottom: auto;
                right: -47px;
                top: 0;
                transform: translateX(-50%);
                max-width: 90px;
                height: auto;
            }
        }
    }
</style>

<script>
    import axios from 'axios'
    import 'leaflet/dist/leaflet.css'
    import { map, tileLayer, marker, icon } from 'leaflet'
    let myMap;

    export default {
        data() {
            return {
                datapoints: [],
                currentDatapoint: null
            }
        },
        created() {
            axios.get('/data/current').then(r => {
                this.currentDatapoint = r.data

                myMap.setView([
                    this.currentDatapoint.latitude, 
                    this.currentDatapoint.longitude
                ], 7)

                let markerIcon = icon({
                    iconUrl: '/static/icon.png',
                    //iconSize: [128, 128],
                    //iconAnchor: [20, 90],
                    iconSize: [64, 64],
                    iconAnchor: [10, 45],
                    popupAnchor: [-3, -76],
                    //shadowUrl: 'my-icon-shadow.png',
                    //shadowSize: [68, 95],
                    //shadowAnchor: [22, 94]
                })

                marker([
                    this.currentDatapoint.latitude, 
                    this.currentDatapoint.longitude
                ], { icon: markerIcon }).addTo(myMap);
            })
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
        }
    }
</script>