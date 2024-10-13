import React from 'react'
import { Link } from 'react-router-dom';
import '../Login.css';

export default function Login() {
  return (
    <>
      <div className='background'>
        <div className='half'>
          <div className='header'>Log in</div>
          <div>
            <input type='text' name='username' placeholder='Username' maxLength={24}/>
          </div>
          <div>
            <input type='password' name='password' placeholder='Password' maxLength={40}/>
          </div>
        </div>
        <div className='half'>
          <button className='logIn'>Log In</button>
          <div>Don't have an Account? <Link to='/signup' className='login'>Sign Up</Link></div>
        </div>
      </div>
    </>
  )
}
