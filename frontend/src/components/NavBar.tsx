import { useAuthContext } from "../context/AuthContext";
import './NavBar.css';

export const NavBar = () => {
    const { logout } = useAuthContext();
    
    return (
        <header className="navbar">
            <div className="navbar-logo">SPA Comments</div>
            <button className="logout-button" onClick={logout}>Log Out</button>
        </header>
    );
};