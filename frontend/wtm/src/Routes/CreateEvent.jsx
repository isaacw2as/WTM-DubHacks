import React, { useState } from 'react';
import '../CreateEvent.css';
import { useNavigate } from 'react-router';
import axios from "axios"
import { CREATE_EVENT_ENDPOINT } from '../endpoints';

export default function CreateEvent({loggedInUser}) {
  const [eventName, setEventName] = useState("")
  const [date, setDate] = useState("")
  const [time, setTime] = useState('')
  const [location, setLocation] = useState("")
  const [description, setDescription] = useState("")
  const [tags, setTags] = useState("")
  const nav = useNavigate()

  const onChangeName = (e) => {
    setEventName(e.target.value)
  }

  const onChangeDate = (e) => {
    setDate(e.target.value)
  }

  const onChangeTime = (e) => {
    setTime(e.target.value)
  }

  const onChangeLocation = (e) => {
    setLocation(e.target.value)
  }

  const onChangeDescription = (e) => {
    setDescription(e.target.value)
  }

  const onChangeTags = (e) => {
    setTags(e.target.value)
  }

  const handleSubmit = async () => {
    if (!eventName || !location || !description || !tags || !date || !time) {
      return;
    }

    let time_string;
    try {
      const split_date = date.split("/");
      const [month, day, year] = split_date.map((num) => parseInt(num));
      if (month < 1 || 12 < month || day < 1 || 31 < day || year < 1) {
        return;
      }

      const [hours, minutes] = time.split(":")
      
      time_string = `${year}-${month}-${day}T${hours}:${minutes}`
    } catch (error) {
      console.log("bad date / time formatting")
      return
    }

    const interests = tags.split(",")
    axios.post(CREATE_EVENT_ENDPOINT, {
      username: loggedInUser,
      event_name: eventName,
      location: location,
      timestamp: time_string,
      description: description,
      interests: interests,
    }).then(() => {
      nav("/createpost")
    }).catch((error) => {
      console.log("error occurred when creating event")
    })
  }

  return (
    <>
      <div className='eventpage'>
        <div className='Navbar'>

        </div>
        <div className='centerContent'>
          <div className='eventHeader'>Create Your Event</div>
          <div>
            <p className='eventParagraph'>Event Name</p>
            <input onChange={onChangeName} type='text' className='eventLongBox' name='username' placeholder='Name of Your Amazing Event ' maxLength={24}/>
          </div>
          <div>
            <p className='eventParagraph'>Time</p>
            <input onChange={onChangeDate} type='text' className='eventShortBox' name='day' placeholder='MM/DD/YYYY' maxLength={10}/>
            <input onChange={onChangeTime} type='text' className='eventShortBox' name='starttime' placeholder='HH:MM' maxLength={5}/>
          </div>
          <div>
            <p className='eventParagraph'>Location</p>
            <input onChange={onChangeLocation} type='text' className='eventLongBox' name='location' placeholder='Where is your event happening?' maxLength={30}/>
          </div>
          <div>
            <p className='eventParagraph'>Description</p>
            <input onChange={onChangeDescription} type='text' className='eventLongBox' name='description' placeholder={`Event description--what's the move?`} maxLength={30}/>
          </div>
          <div>
            <p className='eventParagraph'>Tags</p>
            <input onChange={onChangeTags} type='text' className='eventLongBox' name='tags' placeholder='Type in keywords people can use to find your event.' maxLength={30}/>
          </div>
          <button className='createButton' onClick={handleSubmit}>Create</button>
        </div>
      </div>
    </>
    // make button change color when clicked (button:click)
  )
}
