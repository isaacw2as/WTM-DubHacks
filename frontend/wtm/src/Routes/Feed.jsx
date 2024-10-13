import React, { useState, useEffect } from 'react'
import axios from "axios"
import { GET_FEED_ENDPOINT } from "../endpoints"

export default function Feed({loggedInUser}) {
  const [feed, setFeed] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isVideo, setIsVideo] = useState(null)
  const [currentContent, setCurrentContent] = useState(null)

  const fetchFeed = async () => {
    const result = await axios.get(GET_FEED_ENDPOINT, { params: { loggedInUser: loggedInUser } })
    console.log(result)
    return result
  }

  useEffect(() => {
    console.log("Hitting endpoint")
    const initFeed = fetchFeed()
    setFeed(initFeed)
    setIsLoading(false)
  }, [])

  useEffect(() => {
    if (feed.length() <= 1) {
      const additionalFeed = fetchFeed()
      setFeed(feed.concat(additionalFeed))
    }
  }, [feed])

  return (
    <>
      {
        isLoading
        ? 
        <div>IM LOADING!!!</div>
        :
        
        isVideo 
        ?
        <video src={getSrc(toDownload)} width="320" height="240" autoPlay loop controls>
          Your browser does not support the video tag.
        </video>
        :
        <img src={getSrc(toDownload)}></img>
      }
      <button>go next!</button>
    </>
  )
}
