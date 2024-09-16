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
        navigate('/')
    };

    return (
        <div>
            {loginButton ? (
                <div className="buttonGroup">
                    <button className="btn btn-light btn-lg" onClick={handleLogout}>Logout</button>
                    <Link to='/'><button className="btn btn-light btn-lg mx-2">Home</button></Link>
                </div>
            ) : (
                <div className="buttonGroup">
                    <Link to='/login'><button className="btn btn-light btn-lg" data-abc="true">Login</button></Link>
                    <Link to='/'><button className="btn btn-light btn-lg mx-2">Home</button></Link>
                </div>
            )}
            <Outlet />
        </div>
    )
}
