<template>
    <v-row justify="center">
        <v-col cols="12" md="12" lg="12" xl="10">
            <Podium :images="images">
                <template
                    v-for="(user, i) in podiumPlaces"
                    v-slot:[`title.${i}`]="{ place }"
                >
                    <span class="float-left">{{ place }}.</span>
                    {{ user.full_name }}
                    <span class="float-right">{{ user.theses_count }}</span>
                </template>
            </Podium>
            <v-container fluid>
                <v-row justify="space-around" align="start">
                    <v-col cols="12" sm="6" lg="3" v-for="(items, i) in nextPlaces" :key="i">
                        <v-card>
                            <v-list>
                                <v-list-item
                                    v-for="(user, i) in items"
                                    :key="i"
                                >
                                    <v-list-item-avatar>
                                        <v-img :src="imgLink(user)"></v-img>
                                    </v-list-item-avatar>
                                    <v-list-item-content>
                                        <v-list-item-title>
                                            {{ user.full_name }}
                                            <span class="float-right body-1">{{ user.theses_count }}</span>
                                        </v-list-item-title>
                                    </v-list-item-content>
                                </v-list-item>
                            </v-list>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-col>
    </v-row>
</template>

<script type="text/tsx">
    import _ from 'lodash';
    import Vue from 'vue';
    import Axios from '../../axios';
    import Podium from './Podidum';

    export default Vue.extend({
        name: 'Page',
        components: {Podium},
        data() {
            return {
                results: []
            };
        },
        computed: {
            podiumPlaces() {
                return this.results.slice(0, 3);
            },
            nextPlaces() {
                return _.chunk(this.results.slice(3, 23), 5);
            },
            images() {
                return _.map(this.podiumPlaces, this.imgLink);
            }
        },
        methods: {
            imgLink({username}) {
                return `https://www.spseol.cz/images/kontakty/${username.split('.')[0]}.jpg`;
            }
        },
        async created() {
            this.results = (await Axios.get('/api/v1/theses-competition')).data;
        }
    });
</script>

<style scoped>

</style>