// TODO: https://pypi.org/project/django-typomatic/
export declare class User extends Object {
    id: number;
    username: string;
    full_name: string;
}

export declare class TypeAttachment extends Object {
    name: string;
    identifier: string;
}

export declare class Attachment extends Object {
    id: string;
    url: string;
    size_label: string;
    type_attachment: TypeAttachment;
}


export declare class Reservation extends Object {
    id: string;
    thesis: string;
    user: User;
    thesis_label: string;
    thesis_registration_number: string;
    created: string;
    state: string;
    state_label: string;
}

export declare class Thesis extends Object {
    id: string;
    title: string;
    abstract: string;
    registration_number: string;
    supervisor: User;
    opponent: User;
    authors: Array<User>;
    attachments: Array<Attachment>;
    reviews: Array<object>;

    state: string;
    state_label: string;

    available_for_reservation: boolean;
    reservable: boolean;
    open_reservations_count: number;
}