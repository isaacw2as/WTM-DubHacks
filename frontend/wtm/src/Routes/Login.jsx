import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom';
import '../Login.css';
import { LOGIN_ENDPOINT } from '../endpoints';
import axios from "axios"

export default function Login({ setLoggedInUser }) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const nav = useNavigate();

  const onChangeUsername = (e) => {
    setUsername(e.target.value)
  }

  const onChangePassword = (e) => {
    setPassword(e.target.value)
  }

  const handleLogin = async () => {
    if (username && password) {
      axios.post(LOGIN_ENDPOINT, {username: username, password: password})
      .then((res) => {
        setLoggedInUser(username)
        nav("/feed")
      }).catch((error) => {
        console.log("Unable to login")
      })
    }
  }

  return (
    <>
      <div className='background'>
        <div className='loginhalf'>
          <div className='header'>Log in</div>
          <div>
            <input type='text' name='username' placeholder='Username' maxLength={24} onChange={onChangeUsername}/>
          </div>
          <div>
            <input type='password' name='password' placeholder='Password' maxLength={40} onChange={onChangePassword}/>
          </div>
        </div>
        <div className='loginhalf'>
          <button className='logIn' onClick={handleLogin}>Log In</button>
          <div>Don't have an Account? <Link to='/signup' className='login'>Sign Up</Link></div>
        </div>
        {/*Make sure I figure out if user signed up but didnt choose interests yet (closed page for example, login takes them to interests) */}
        {/*Make sure button changes color to my choice when hovered, then black when clicked*/}
      </div>
    </>
  )
}
