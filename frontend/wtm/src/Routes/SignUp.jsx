import React from 'react';
import { Link } from 'react-router-dom';
//<Link to ={user.id}>{user.name}</Link>
import '../SignUp.css';

export default function SignUp({ }) {
  return (
    <>
      <div className='background'>
        <div className='half'>
          <div className='header'>Sign Up</div>
          <div>
            <input type='text' name='username' placeholder='Username' maxLength={24}/>
          </div>
          <div>
            <input type='passsword' name='password' placeholder='Password' maxLength={40}/>
          </div>
        </div>
        <div className='half'>
          <button className='createAccount'>Create An Account</button>
          <div>Have an Account? <span className='login'>Log In</span></div>
        </div>
      </div>
    </>
    // make button change color when clicked (button:click)
  )
}
