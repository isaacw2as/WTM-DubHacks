import React from 'react';
import { Link } from 'react-router-dom';
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
            <input type='password' name='password' placeholder='Password' maxLength={40}/>
          </div>
        </div>
        <div className='half'>
          <button className='createAccount'>Create An Account</button>
          <div>Have an Account? <Link to='/' className='login'>Log In</Link></div>
        </div>
      </div>
    </>
    // make button change color when clicked (button:click)
  )
}
