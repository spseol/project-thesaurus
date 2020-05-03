<template>
    <v-container fluid class="body-1">
        <v-row no-gutters>
            <v-col cols="12" md="9" lg="8" xl="6">
                <v-row
                    v-for="[title, getter, titleCss = '', valueCss = ''] in rows" v-if="getByGetter(getter)"
                    :key="getter.toString()" no-gutters>
                    <v-col cols="12" md="1" class="font-weight-bold text-left text-md-right" :class="titleCss">
                        {{ title }}
                    </v-col>
                    <v-col class="text-justify" :class="valueCss">
                        <p class="text-justify pl-3">
                            {{ getByGetter(getter) }}
                        </p>
                    </v-col>
                </v-row>
                <v-row v-for="attachment in thesis.attachments" :key="attachment.id">
                    <v-col cols="12" md="1" class="text-left text-md-right">
                        <v-icon>mdi-pdf-box</v-icon>
                    </v-col>
                    <v-col>
                        <p class="text-justify pl-3">
                            <a :href="attachment.url">{{ attachment.type_attachment.name }}</a>
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
                    [this.$t('Author'), (t) => _.map(t.authors, 'full_name').join(', ')],
                    [this.$t('Supervisor'), 'supervisor.full_name'],
                    [this.$t('Opponent'), 'opponent.full_name'],
                    [this.$t('Year'), 'published_at'],
                    [this.$t('Category'), 'category.title'],
                    [this.$t('Abstract'), 'abstract'],
                ],
            };
        },
        methods: {
            getByGetter(getter) {
                return _.isFunction(getter) ? getter(this.thesis) : _.get(this.thesis, getter, '');
            },
        },
    };
</script>