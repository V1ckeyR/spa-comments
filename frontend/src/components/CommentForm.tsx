import { Paperclip, ALargeSmallIcon, Bold, Italic, Link, Code } from 'lucide-react';
import React, { useState } from 'react';

interface CommentFormProps {
    onSubmit: (content: string) => void;
    onClose: () => void;
}


export const CommentForm: React.FC<CommentFormProps> = ({ onSubmit, onClose }) => {
    const [content, setContent] = useState('');

    const handleSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!content.trim()) return;
        console.log(content);

        onSubmit(content);
        setContent('');
        onClose();
    };

    return (
        <div className='comment-form'>
            <form onSubmit={handleSubmit}>
                <textarea 
                    value={content} 
                    onChange={(e) => setContent(e.target.value)} 
                    placeholder="Add a comment"
                    required
                    minLength={3}
                    maxLength={1000}
                />
                <div className='comment-form-footer'>
                    <div className='comment-form-actions'>
                        <button 
                            className='icon-button'
                            title='Add an attachment'
                        >
                            <Paperclip />
                        </button>
                        <button
                            className='icon-button'
                            title='Apply bold formatting'
                        >
                            <Bold />
                        </button>
                        
                        <button
                            className='icon-button'
                            title='Apply italic formatting'
                        >
                            <Italic />
                        </button>
                        
                        <button
                            className='icon-button'
                            title='Create link'
                        >
                            <Link />
                        </button>
                        
                        <button
                            className='icon-button'
                            title='Apply code formatting'
                        >
                            <Code />
                        </button>
                        
                    </div>
                    <div className='comment-form-actions'>
                        <input type='button' value='Cancel' onClick={onClose}/>
                        <input type="submit" value='Submit' className='primary-button'/>
                    </div>
                </div>
            </form>
        </div>
    );
};