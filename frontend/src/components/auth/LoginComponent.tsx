import {useState, FormEvent, useContext, FC} from 'react';
import {useNavigate} from 'react-router-dom';
import {requestTemplate} from '../../request/axiosRequest';
import {LoginButtonContext} from '../../contexts/auth/LoginButtonContext';
import '../../styles/auth/login.css';


const LoginComponent: FC = () => {
    const {loginButton, setLoginButton} = useContext(LoginButtonContext);
    let navigate = useNavigate()
    const [formData, setFormData] = useState({
        username: '',
        password: '',

    });
    const handleEmailChange = (event: FormEvent<HTMLInputElement>) => {
        setFormData({...formData, 'username': (event.target as HTMLInputElement).value});
    };
    const handlePasswordChange = (event: FormEvent<HTMLInputElement>) => {
        setFormData({...formData, 'password': (event.target as HTMLInputElement).value});
    };


    const submitHandler = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        requestTemplate.post('api/auth/login', new URLSearchParams(formData))
            .then(response => {
                localStorage.setItem('access', response.data.access_token)
                setLoginButton(true)
                navigate('/')
            })
            .catch(error => {
                alert('Wrong username or password');
            });
    };

    return (
        <div className="login-container">
            <form onSubmit={submitHandler}>
                <div><input className="login-input" type="text" name="username" placeholder="username"
                            onChange={handleEmailChange}/></div>
                <div><input className="login-input" type="password" name="password"
                            placeholder="Password" onChange={handlePasswordChange}/></div>
                <button className="login-button">Log In</button>
            </form>
        </div>

    )
}

export default LoginComponent;
