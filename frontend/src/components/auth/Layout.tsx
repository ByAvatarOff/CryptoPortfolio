import { Outlet } from "react-router-dom"
import { Link, useNavigate } from 'react-router-dom';
import { LoginButtonContext } from "../../contexts/auth/LoginButtonContext";
import { useContext } from "react";
import '../../styles/auth/layout.css';

export const Layout = () => {
    const { loginButton, setLoginButton } = useContext(LoginButtonContext);
    const navigate = useNavigate()

    const handleLogout = () => {
        setLoginButton(false)
        localStorage.clear()
        navigate('/login')
    };

    return (
        <div>
            {loginButton ? (
                <div className="auth-container">
                    <button className="button-logout" onClick={handleLogout}>Logout</button>
                </div>
            ) : (
                <div></div>
            )}
            <Outlet />
        </div>
    )
}
