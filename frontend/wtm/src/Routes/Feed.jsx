import React, { useState, useEffect } from 'react'
import axios from "axios"
import { GET_FEED_ENDPOINT } from "../endpoints"

export default function Feed({loggedInUser}) {
  const [feed, setFeed] = useState(null);

  const fetchFeed = async () => {
    // const result = await axios.get(GET_FEED_ENDPOINT, { params: { loggedInUser: loggedInUser } })
    // console.log(result)
  }

  useEffect(() => {
    console.log("Hitting endpoint")
    fetchFeed()
  }, [])


  return (
    <div>
      Hello world!
    </div>
  )
}
