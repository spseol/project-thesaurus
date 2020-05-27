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
                        <td class="font-weight-bold text-left text-md-right col-1">{{ $t('Author') }}</td>
                        <td>{{ thesis.authors.map(o => o.full_name).join(', ') }}</td>
                    </tr>
                    <tr v-if="thesis.supervisor">
                        <td class="font-weight-bold text-left text-md-right col-1">{{ $t('Supervisor') }}</td>
                        <td>{{ thesis.supervisor.full_name }}</td>
                    </tr>
                    <tr v-if="thesis.opponent">
                        <td class="font-weight-bold text-left text-md-right col-1">{{ $t('Opponent') }}</td>
                        <td>{{ thesis.opponent.full_name }}</td>
                    </tr>
                    <tr>
                        <td class="font-weight-bold text-left text-md-right col-1">{{ $t('Year') }}</td>
                        <td>{{ thesis.published_at }}</td>
                    </tr>
                    <tr>
                        <td class="font-weight-bold text-left text-md-right col-1">{{ $t('Category') }}</td>
                        <td>{{ thesis.category.title }}</td>
                    </tr>
                    <tr v-has-perm:thesis.change_thesis>
                        <td class="font-weight-bold text-left text-md-right col-1">{{ $t('SN') }}</td>
                        <td>{{ thesis.registration_number }}</td>
                    </tr>
                    <tr v-if="thesis.abstract">
                        <td class="font-weight-bold text-left text-md-right col-1">{{ $t('Abstract') }}</td>
                        <td class="py-1">{{ thesis.abstract }}</td>
                    </tr>

                    <tr v-if="$asyncComputed.attachments.updating || $asyncComputed.reviews.updating">
                        <td colspan="2">
                            <v-progress-linear indeterminate color="grey"></v-progress-linear>
                        </td>
                    </tr>

                    <tr v-for="attachment in attachments">
                        <td class="text-left text-md-right">
                            <v-icon>${{ attachment.type_attachment.identifier }}</v-icon>
                        </td>
                        <td>
                            <v-btn small outlined color="primary" :href="attachment.url" target="_blank">
                                {{ attachment.type_attachment.name }}

                                <!--                                <v-icon class="ml-2">mdi-share-outline</v-icon>-->
                            </v-btn>
                        </td>
                    </tr>

                    <tr v-for="review in reviews">
                        <td class="text-left text-md-right">
                            <v-icon>mdi-book-information-variant</v-icon>
                        </td>
                        <td>
                            <v-btn small outlined color="primary"
                                :to="$i18nRoute({
                                        name: 'review-detail',
                                        params: {thesisId: thesis.id, reviewId: review.id}
                                    })"
                            >
                                {{ $t('Review') }} {{ review.user.full_name || review.user.username }}
                            </v-btn>

                            <v-btn
                                :href="review.url" v-if="showPdfReviews"
                                small outlined color="info" target="_blank"
                            >
                                {{ $t('Review PDF detail') }} {{ review.user.full_name || review.user.username }}
                            </v-btn>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </v-col>
            <v-col cols="12" md="4" class="align-center d-flex justify-center">
                <v-progress-circular
                    indeterminate
                    v-if="$asyncComputed.attachments.updating"
                ></v-progress-circular>

                <v-dialog v-if="poster" max-width="70vw" max-height="90vh">
                    <template v-slot:activator="{ on }">
                        <v-img
                            :src="poster.url" v-on="on"
                            max-width="300px" class="elevation-2"
                        ></v-img>
                    </template>

                    <v-row no-gutters justify="space-around">
                        <v-img
                            :src="poster.url" v-on="on"
                            max-width="70vw" max-height="90vh"
                        ></v-img>
                    </v-row>
                </v-dialog>
            </v-col>
        </v-row>
    </v-container>

</template>
<script type="text/tsx">
    import _ from 'lodash';
    import Axios from '../../axios';
    import {hasPerm} from '../../user';
    import {pageContext} from '../../utils';

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
                return _.find(this.attachments, {type_attachment: {identifier: 'thesis_poster'}});
            },
            showPdfReviews() {
                return this.hasAddReviewPerm || !!_.find(this.thesis.authors, {id: pageContext.user.id});
            }
        },
        asyncComputed: {
            hasAddReviewPerm: {
                get() {
                    return hasPerm('review.add_review');
                },
                default: false
            },
            reviews: {
                get() {
                    if (this.thesis.reviews) return new Promise((r) => r(this.thesis.reviews));
                    return Axios.get(`/api/v1/thesis/${this.thesis.id}/reviews`).then(r => r.data);
                },
                default: []
            },
            attachments: {
                get() {
                    if (this.thesis.attachments) return new Promise((r) => r(this.thesis.attachments));
                    return Axios.get(`/api/v1/thesis/${this.thesis.id}/attachments`).then(r => r.data);
                },
                default: []
            }
        }
    };
</script>