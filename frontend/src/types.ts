export interface User {
    id: number;
    username: string;
    email: string;
    home_page?: string | null;
    avatar?: string | null;
    created_at: string;
    updated_at: string;
}

export interface Attachment {
    id: number;
    url: string;
    comment: number;
    created_at: string;
    updated_at: string;
}

export interface Reaction {
    id: number;
    user: User;
    comment: number;
    reaction: number;
}

export interface Comment {
    id: number;
    content: string;
    user: User;
    reply_to?: number | null;
    created_at: string;
    updated_at: string;

    replies?: Comment[];
    reactions?: Reaction[];
    attachments?: Attachment[];
}
