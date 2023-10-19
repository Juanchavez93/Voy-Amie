import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function TripDetail() {
  let params = useParams();
  let paramsInt = parseInt(params.trip_id);
  const [activities, setActivities] = useState([]);
  const [formData, setFormData] = useState({
    title: "",
    url: "",
    date: "",
    time: "",
  });
  const [comments, setComments] = useState([]);
  const [formCommentData, setFormCommentData] = useState({
    comment: "",
  });

  const getActivitiesData = async () => {
    const activitiesUrl = `${process.env.REACT_APP_API_HOST}/activities/`;
    const response = await fetch(activitiesUrl, {
      credentials: "include",
    });
    if (response.ok) {
      const data = await response.json();
      console.log(data);
      setActivities(data);
    }
  };

  const getCommentsData = async () => {
    const commentsUrl = `${process.env.REACT_APP_API_HOST}/comments?trip=${paramsInt}`;
    const response = await fetch(commentsUrl, {
      credentials: "include",
    });
    if (response.ok) {
      const commentsData = await response.json();
      console.log(commentsData);
      setComments(commentsData);
    }
  };

  useEffect(() => {
    getActivitiesData();
    getCommentsData();
  }, []); //eslint-disable-line react-hooks/exhaustive-deps

  const handleUpvote = async (
    activity_id,
    title,
    url,
    date,
    time,
    status,
    vote
  ) => {
    await fetch(`${process.env.REACT_APP_API_HOST}/activities/${activity_id}`, {
      method: "PUT",
      body: JSON.stringify({
        trip: paramsInt,
        title: title,
        url: url,
        date: date,
        time: time,
        status: status,
        vote: vote + 1,
      }),
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    });
    getActivitiesData();
  };

  const handleDownvote = async (
    activity_id,
    title,
    url,
    date,
    time,
    status,
    vote
  ) => {
    await fetch(`${process.env.REACT_APP_API_HOST}/activities/${activity_id}`, {
      method: "PUT",
      body: JSON.stringify({
        trip: paramsInt,
        title: title,
        url: url,
        date: date,
        time: time,
        status: status,
        vote: vote - 1,
      }),
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    });
    getActivitiesData();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const activityURL = `${process.env.REACT_APP_API_HOST}/activity/`;
    const fetchConfig = {
      method: "post",
      body: JSON.stringify(
        formData,
        (formData["status"] = "PENDING"),
        (formData["vote"] = 0),
        (formData["trip"] = paramsInt)
      ),
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    };

    const response = await fetch(activityURL, fetchConfig);
    if (response.ok) {
      const newActivity = await response.json();
      console.log(newActivity);

      setFormData({
        title: "",
        url: "",
        date: "",
        time: "",
      });
    }
    getActivitiesData();
  };

  const handleFormChange = (e) => {
    const value = e.target.value;
    const inputName = e.target.name;
    setFormData({
      ...formData,

      [inputName]: value,
    });
  };

  const handleCommentSubmit = async (e) => {
    e.preventDefault();

    const commentURL = `${process.env.REACT_APP_API_HOST}/comments/`;
    const fetchConfig = {
      method: "post",
      body: JSON.stringify(
        formCommentData,
        (formCommentData["trip"] = paramsInt)
      ),
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    };

    const response = await fetch(commentURL, fetchConfig);
    if (response.ok) {
      const newActivity = await response.json();
      console.log(newActivity);

      setFormCommentData({
        comment: "",
      });
    }
    getCommentsData();
  };

  const handleCommentFormChange = (e) => {
    const value = e.target.value;
    const inputName = e.target.name;
    setFormCommentData({
      ...formCommentData,

      [inputName]: value,
    });
  };

  return (
    <>
      <h1>Trip ID: {params.trip_id}</h1>
      <div className="shadow p-4 mt-4">
        <h1>Add An Activity</h1>
        <form onSubmit={handleSubmit} id="create-customer-form">
          <div className="form-floating mb-3">
            <input
              value={formData.title}
              onChange={handleFormChange}
              placeholder="Title"
              required
              type="text"
              id="title"
              name="title"
              className="form-control"
            />
            <label htmlFor="title">Title</label>
          </div>
          <div className="form-floating mb-3">
            <input
              value={formData.url}
              onChange={handleFormChange}
              placeholder="URL"
              required
              type="text"
              id="url"
              name="url"
              className="form-control"
            />
            <label htmlFor="url">URL</label>
          </div>
          <div className="form-floating mb-3">
            <input
              value={formData.date}
              onChange={handleFormChange}
              placeholder="Date"
              required
              type="text"
              id="date"
              name="date"
              className="form-control"
              maxLength={14}
            />

            <label htmlFor="date">Date</label>
          </div>
          <div className="form-floating mb-3">
            <input
              value={formData.time}
              onChange={handleFormChange}
              placeholder="Time"
              required
              type="text"
              id="time"
              name="time"
              className="form-control"
            />
            <label htmlFor="">Time</label>
          </div>
          <button className="btn btn-primary">Create</button>
        </form>
      </div>
      <h2>Comments</h2>
      <table>
        <thead>
          <tr>
            <th>Commenter</th>
            <th>Comment</th>
          </tr>
        </thead>
        <tbody>
          {comments.map((comments) => {
            return (
              <tr key={comments.comment_id}>
                <td>{comments.commenter}</td>
                <td>{comments.comment}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <h2>Activities</h2>
      <table>
        <thead>
          <tr>
            <td>Title</td>
            <td>Date</td>
            <td>Time</td>
            <td>Status</td>
            <td>Vote Count</td>
            <td>Vote!</td>
          </tr>
        </thead>
        <tbody>
          {activities.map((activities) => {
            if (paramsInt === activities.trip) {
              return (
                <>
                  <tr key={activities.activity_id}>
                    <td className="text-center align-middle">
                      {activities.title}
                    </td>
                    <td>{activities.date}</td>
                    <td>{activities.time}</td>
                    <td>{activities.status}</td>
                    <td>{activities.vote}</td>
                    <button
                      onClick={() =>
                        handleUpvote(
                          activities.activity_id,
                          activities.title,
                          activities.url,
                          activities.date,
                          activities.time,
                          activities.status,
                          activities.vote
                        )
                      }
                    >
                      Yes
                    </button>
                    <button
                      onClick={() =>
                        handleDownvote(
                          activities.activity_id,
                          activities.title,
                          activities.url,
                          activities.date,
                          activities.time,
                          activities.status,
                          activities.vote
                        )
                      }
                    >
                      No
                    </button>
                  </tr>
                </>
              );
            } else {
              return null;
            }
          })}
        </tbody>
      </table>
      <div className="shadow p-4 mt-4">
        <h1>Add A Comment</h1>
        <form onSubmit={handleCommentSubmit} id="create-customer-form">
          <div className="form-floating mb-3">
            <input
              value={formCommentData.comment}
              onChange={handleCommentFormChange}
              placeholder="Comment"
              required
              type="text"
              id="comment"
              name="comment"
              className="form-control"
            />
            <label htmlFor="comment">Comment</label>
          </div>
          <button className="btn btn-primary">Create</button>
        </form>
      </div>
    </>
  );
}

export default TripDetail;