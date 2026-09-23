import React, { useState } from 'react';
import type { Comment } from '../types';
import { CommentForm } from './CommentForm';
import { formatDate } from '../utils/datetime';

import { Hash, Bookmark, ArrowRightFromLine, CircleArrowUp, CircleArrowDown, ArrowUp, ArrowDown } from 'lucide-react';

interface CommentItemProps {
    comment: Comment;
}

const DEFAULT_AVATAR = 'https://t4.ftcdn.net/jpg/07/03/86/11/360_F_703861114_7YxIPnoH8NfmbyEffOziaXy0EO1NpRHD.jpg';

export const CommentItem: React.FC<CommentItemProps> = ({ comment }) => {
    const [isReplyFormOpen, setIsReplyFormOpen] = useState(false);
    const [isThreadOpen, setIsThreadOpen] = useState(true);
    const totalScore = comment.reactions ? comment.reactions.reduce((acc, curr) => acc + curr.reaction, 0) : 0

    return (
        <div className='comment-card'>
        <div className='comment-header'>
          <div className='comment-user-info'>
            <img 
              src={comment.user.avatar || DEFAULT_AVATAR}
              alt={comment.user.username}
              className='avatar'/>
            <span className='username'>{comment.user.username}</span>
            <span className='date'>{formatDate(comment.created_at)}</span>
            <Hash />
            <Bookmark />
            <ArrowRightFromLine onClick={() => setIsReplyFormOpen(true)} />
            {comment.replies && comment.replies.length > 0 && (
              <button 
                className="icon-button" 
                onClick={() => setIsThreadOpen(!isThreadOpen)}
              >
                {isThreadOpen ? <CircleArrowUp /> : <CircleArrowDown />}
              </button>
            )}
          </div>
          <div className='comment-reactions'>
            <ArrowUp />
            {totalScore}
            <ArrowDown />
          </div>
        </div>
  
        {/* Main comment content */}
        <p className='comment-content'>{comment.content}</p>
        {isReplyFormOpen && <CommentForm onSubmit={() => {}} onClose={() => setIsReplyFormOpen(false)} />}

  
        {/* Recursive step: Render nested replies if they exist */}
        {isThreadOpen && comment.replies && comment.replies.length > 0 && (
          <div className='comment-replies'>
            {comment.replies.map((reply) => (
                <CommentItem key={reply.id} comment={reply} />
            ))}
          </div>
        )}
      </div>
    );
};