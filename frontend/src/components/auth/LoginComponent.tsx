import { useState, FormEvent, useContext, FC } from 'react';
import { useNavigate } from 'react-router-dom';
import { requestTemplate } from '../../request/axiosRequest';
import { LoginButtonContext } from './LoginButtonContext';



const LoginComponent: FC = () => {
  const { loginButton, setLoginButton } = useContext(LoginButtonContext);
  let navigate = useNavigate()
  const [formData, setFormData] = useState({
    username: '',
    password: '',

  });
  const handleEmailChange = (event: FormEvent<HTMLInputElement>) => {
    setFormData({ ...formData, 'username': (event.target as HTMLInputElement).value });
  };
  const handlePasswordChange = (event: FormEvent<HTMLInputElement>) => {
    setFormData({ ...formData, 'password': (event.target as HTMLInputElement).value });
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
    <div className="container mt-5" style={{ width: "400px", height: "600px" }}>
      <form onSubmit={submitHandler}>
        <h2 className="sr-only">Login Form</h2>
        <div className="form-group"><input className="form-control" type="text" name="username" placeholder="username" onChange={handleEmailChange} /></div>
        <div className="form-group"><input className="form-control" type="password" name="password"
          placeholder="Password" onChange={handlePasswordChange} />
        </div>
        <div className="form-group"><button className="btn btn-primary btn-block">Log In</button></div>
      </form>
    </div>

  )
}

export default LoginComponent;
