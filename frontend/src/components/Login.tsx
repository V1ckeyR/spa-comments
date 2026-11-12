import { useState } from "react";
import { useAuthContext } from "../context/AuthContext";
import './Login.css';
import axios from "axios";

export const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useAuthContext();

    const handleSubmit = async (e: React.SubmitEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            await login(username, password);
        } catch (error) {
            if (axios.isAxiosError(error)) {
                if (!error.response) {
                    setError('Cannot connect to the server. Please try again later.');
                } else if (error.response.status === 401) {
                    setError('Invalid username or password');
                } else {
                    setError('Something went wrong. Please try again later.');
                }
            } else {
                setError('An error occurred. Please try again later.');
            }
        } finally {
            setLoading(false);
        }    
    };

    return (
        <div className="login-container">
            <form className="login-form" onSubmit={handleSubmit}>
                <h2>Login</h2>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                {error && <p className="error-message">{error}</p>}
                <button type="submit" disabled={loading}>Login</button>
                <p className="login-form-links">
                    <a href="/register">Don't have an account?</a>
                    <a href="/reset-password">Forgot password?</a>
                </p>
            </form>
        </div>
    );
};