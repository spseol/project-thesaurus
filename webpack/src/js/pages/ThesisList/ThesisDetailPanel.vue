<template>
    <v-container fluid class="body-1">
        <v-row no-gutters>
            <v-col cols="12" md="8">
                <table class="InfoTable">
                    <tbody>
                    <tr>
                        <td colspan="2" class="display-1">{{ thesis.title }}</td>
                    </tr>
                    <tr>
                        <td class="font-weight-bold text-left text-md-right col-md-1">{{ $t('Author') }}</td>
                        <td>{{ thesis.authors.map(o => o.full_name).join(', ') }}</td>
                    </tr>
                    <tr v-if="thesis.supervisor">
                        <td class="font-weight-bold text-left text-md-right col-md-1">{{ $t('Supervisor') }}</td>
                        <td>{{ thesis.supervisor.full_name }}</td>
                    </tr>
                    <tr v-if="thesis.opponent">
                        <td class="font-weight-bold text-left text-md-right col-md-1">{{ $t('Opponent') }}</td>
                        <td>{{ thesis.opponent.full_name }}</td>
                    </tr>
                    <tr>
                        <td class="font-weight-bold text-left text-md-right col-md-1">{{ $t('Year') }}</td>
                        <td>{{ thesis.published_at }}</td>
                    </tr>
                    <tr>
                        <td class="font-weight-bold text-left text-md-right col-md-1">{{ $t('Category') }}</td>
                        <td>{{ thesis.category.title }}</td>
                    </tr>
                    <tr v-if="thesis.abstract">
                        <td class="font-weight-bold text-left text-md-right col-md-1">{{ $t('Abstract') }}</td>
                        <td class="text-justify py-1">{{ thesis.abstract }}</td>
                    </tr>
                    <template v-has-perm:attachment.view_attachment>
                        <tr v-for="attachment in thesis.attachments">
                            <td class="text-left text-md-right">
                                <v-icon>${{ attachment.type_attachment.identifier }}</v-icon>
                            </td>
                            <td>
                                <v-btn small outlined color="primary" :href="attachment.url" target="_blank">
                                    {{ attachment.type_attachment.name }}
                                </v-btn>
                            </td>
                        </tr>
                    </template>
                    <template v-has-perm:review.view_review>
                        <tr v-for="review in thesis.reviews">
                            <td class="text-left text-md-right">
                                <v-icon>mdi-book-information-variant</v-icon>
                            </td>
                            <td>
                                <v-btn small outlined color="primary" :to="$i18nRoute({
                                    name: 'review-detail',
                                    params: {thesisId: thesis.id, reviewId: review.id}
                                })">
                                    {{ $t('Review') }}
                                    {{ review.user.full_name || review.user.username }}
                                </v-btn>

                                <v-btn small outlined color="info" :href="review.url" target="_blank">
                                    {{ $t('Review PDF detail') }} {{ review.user.full_name || review.user.username }}
                                </v-btn>
                            </td>
                        </tr>
                    </template>
                    </tbody>
                </table>
            </v-col>
            <v-col cols="12" md="4" class="align-center d-flex justify-center">
                <!--suppress HtmlUnknownTarget -->
                <v-img
                    v-if="poster"
                    :src="poster.url"
                    max-width="300px" class="elevation-2"
                ></v-img>
            </v-col>
        </v-row>
    </v-container>

</template>
<script type="text/tsx">
    import _ from 'lodash';

    export default {
        name: 'ThesisDetailPanel',
        props: {
            thesis: {
                type: Object,
                required: true
            }
        },
        data() {
            return {};
        },
        computed: {
            poster() {
                // TODO: will not work for users without view_attachment perm
                return _.find(this.thesis.attachments, {type_attachment: {identifier: 'thesis_poster'}});
            }
        }
    };
</script>