import React, { useState, useEffect } from 'react'
import axios from "axios"
import { DOWNLOAD_ENDPOINT, GET_FEED_ENDPOINT } from "../endpoints"
import "../Feed.css"

export default function Feed({loggedInUser}) {
  const [feed, setFeed] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isVideo, setIsVideo] = useState(null)

  const initFetchFeed = async () => {
    const result = await axios.get(GET_FEED_ENDPOINT, { params: { username: loggedInUser } })
    const new_feed = result.data

    console.log(new_feed)

    setIsVideo(new_feed[0]["filename"].endsWith(".mov"))
    setFeed(new_feed)
    setIsLoading(false)
  }

  const updateFetchFeed = async () => {
    const result = await axios.get(GET_FEED_ENDPOINT, { params: { username: loggedInUser } })
    const additional_feed = result.data

    console.log(feed.concat(additional_feed))
    setFeed(feed.concat(additional_feed))
  }

  useEffect(() => {
    console.log("Hitting endpoint")
    initFetchFeed()
  }, [])

  useEffect(() => {
    if (feed && feed.length <= 1) {
      const additionalFeed = updateFetchFeed()
      setFeed(feed.concat(additionalFeed))
    }
  }, [feed])

  const handleNext = () => {
    const newFeed = feed.slice(1)
    console.log(newFeed)
    setIsVideo(newFeed[0]["filename"].endsWith(".mov"))
    setFeed(newFeed)
  }

  const getSrc = (filename) => {
    const final = DOWNLOAD_ENDPOINT + "?filename=" + filename
    console.log(final)
    return final
  }

  const get_content = () => {
    return (
      <>
        {
          isLoading
          ? 
          <div>IM LOADING!!!</div>
          :
          isVideo 
          ?
          <video src={getSrc(feed[0]["filename"])} width="500px" height="900px" autoPlay loop controls>
            Your browser does not support the video tag.
          </video>
          :
          <img src={getSrc(feed[0]["filename"])} className={"feed-image"}></img>
        }
      </>
    )
  }


  return (
    <>
      <div className="outer-layout">
        <div className="content">
          {get_content()}
        </div>
        <div className="next_video">
          <button onClick={handleNext}>Next Post!</button>
        </div>
      </div>
    </>
  )
}
