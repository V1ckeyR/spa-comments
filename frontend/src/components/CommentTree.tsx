import React, { useState} from 'react';
import type { Comment } from '../types';
import { CommentItem } from './CommentItem';

const MOCK_COMMENTS: Comment[] = [
    {
        id: 1,
        content: 'This is a comment',
        user: {
            id: 1,
            username: 'John Doe',
            email: 'john.doe@example.com',
            avatar: 'https://thumbs.dreamstime.com/b/generic-male-professional-avatar-icon-business-user-profile-412873474.jpg',
            created_at: '2026-01-01',
            updated_at: '2026-01-01',
        },
        created_at: '2026-01-01',
        updated_at: '2026-01-01',
        replies: [
            {
                id: 2,
                content: 'This is a reply to the first comment',
                user: {
                    id: 2,
                    username: 'Jane Doe',
                    email: 'jane.doe@example.com',
                    created_at: '2026-01-01',
                    updated_at: '2026-01-01',
                },
                reply_to: 1,
                created_at: '2026-01-01',
                updated_at: '2026-01-01',
            },
            {
                id: 3,
                content: 'This is a reply to the second comment',
                user: {
                    id: 3,
                    username: 'Jim Doe',
                    email: 'jim.doe@example.com',
                    avatar: 'https://img.magnific.com/free-vector/woman-with-long-brown-hair-pink-shirt_90220-2940.jpg?semt=ais_hybrid&w=740&q=80',
                    created_at: '2026-01-01',
                    updated_at: '2026-01-01',
                },
                reply_to: 2,
                created_at: '2026-01-01',
                updated_at: '2026-01-01',
                replies: [
                    {
                        id: 4,
                        content: 'This is a reply to the third comment',
                        user: {
                            id: 4,
                            username: 'Jill Doe',
                            email: 'jill.doe@example.com',
                            created_at: '2026-01-01',
                            updated_at: '2026-01-01',
                        },
                        reply_to: 3,
                        created_at: '2026-01-01',
                        updated_at: '2026-01-01',
                    },
                ]
            },
            {
                id: 5,
                content: 'This is a reply to the fourth comment',
                user: {
                    id: 5,
                    username: 'Jack Doe',
                    email: 'jack.doe@example.com',
                    avatar: 'https://img.magnific.com/free-vector/flat-style-woman-face_90220-2936.jpg?semt=ais_hybrid&w=740&q=80',
                    created_at: '2026-01-01',
                    updated_at: '2026-01-01',
                },
                reply_to: 4,
                created_at: '2026-01-01',
                updated_at: '2026-01-01',
            },
        ]
    },
   
];

export const CommentTree: React.FC = () => {
    const [comments] = useState<Comment[]>(MOCK_COMMENTS);

    return (
        <div>
            {comments.map((comment: Comment) => (
                <CommentItem key={comment.id} comment={comment} />
            ))}
        </div>
    );
};