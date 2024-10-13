import React from 'react';
import '../ChooseInterest.css';

export default function SignUp({ }) {
  return (
    <>
      <div className='background'>
        <div className='chooseinterestfirsthalf'>
          <div className='chooseinterestheader'>Welcome!</div>
          <div>
            <p>Select up to 3 types of events you're interested in attending.</p>
          </div>
        <div className='chooseinterestsecondhalf'>
        <div>
            <div>
                <button className='interestbutton'>Art</button>
                <button className='interestbutton'>Music</button>
                <button className='interestbutton'>Gaming</button>
            </div>
            <div>
                <button className='interestbutton'>Nature</button>
                <button className='interestbutton'>Culture</button>
                <button className='interestbutton'>Sports</button>
            </div>
            <div>
                <button className='interestbutton'>Fitness</button>
                <button className='interestbutton'>Travel</button>
                <button className='interestbutton'>Food</button>
            </div>
            {/*FIGURE OUT HOW TO SELECT MULITPLE BUTTONS*/}
            {/*Make sure they have intrests chosen before going to feed, also make sure they cant access feed at all before interests}*/}
        </div>
            <button className='discoverFeed'>Discover</button>
        </div>
        </div>
      </div>
    </>
  )
}
