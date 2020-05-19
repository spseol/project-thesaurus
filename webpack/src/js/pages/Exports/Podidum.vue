<template>
    <v-container fluid>
        <h1 class="text-center display-3">{{ $t('Theses competition') }}</h1>
        <v-divider class="my-3"></v-divider>
        <v-row justify="space-around" align="end">
            <v-col
                v-for="([place, color, height], i) in cards" :key="place"
                cols="10" lg="4" :order="place" :order-lg="i" :order-xl="i" class="d-flex flex-column"
            >
                <v-img
                    v-if="images[place - 1]"
                    :src="images[place - 1]" :width="(70 - place * 10) + '%'"
                    class="align-self-center mb-5 elevation-5"
                ></v-img>
                <v-card>
                    <v-card-title class="d-block">
                        <h1 class="text-center headline">
                            <slot :name="`title.${place - 1}`" :place="place"></slot>
                        </h1>
                    </v-card-title>
                    <v-card-actions :style="{backgroundColor: color, height}"></v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script type="text/tsx">
    import Vue from 'vue';

    export default Vue.extend({
        name: 'Podium',
        props: {
            items: {
                type: Array
            },
            images: {
                type: Array
            }
        },
        data() {
            return {
                cards: [
                    [2, '#c0c0c0', '100px'],
                    [1, '#ffd700', '140px'],
                    [3, '#CD7F32', '60px']
                ]
            };
        }
    });
</script>