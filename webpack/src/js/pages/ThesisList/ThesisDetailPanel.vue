<template>
    <v-container fluid class="body-1">
        <v-row no-gutters>
            <v-col cols="12" md="9" lg="8" xl="6">
                <v-row v-for="[title, path, titleCss = '', valueCss = ''] in rows" :key="path" no-gutters>
                    <v-col cols="12" md="1" class="font-weight-bold text-left text-md-right" :class="titleCss">
                        {{ title }}
                    </v-col>
                    <v-col class="text-justify" :class="valueCss">
                        <p class="text-justify pl-3">
                            {{ getByPath(path) }}
                        </p>
                    </v-col>
                </v-row>
            </v-col>
            <v-col cols="12" md="3" lg="4" xl="6" class="align-center d-flex justify-center">
                <v-img :src="require('../../../img/poster.png')" max-width="200px" class="elevation-2"></v-img>
            </v-col>
        </v-row>
    </v-container>

</template>
<script>
    export default {
        name: 'ThesisDetailPanel',
        props: {
            thesis: {
                type: Object,
                required: true,
            },
        },
        data() {
            return {
                rows: [
                    ['', 'title', null, 'headline'],
                    [this.$t('Author'), 'author.full_name'],
                    [this.$t('Supervisor'), 'supervisor.full_name'],
                    [this.$t('Opponent'), 'opponent.full_name'],
                    [this.$t('Year'), 'published_at'],
                    [this.$t('Category'), 'category.title'],
                    [this.$t('Abstract'), 'abstract'],
                ],
            };
        },
        methods: {
            getByPath(path) {
                return _.get(this.thesis, path, '');
            },
        },
    };
</script>