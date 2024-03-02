
let goDown = false;

function unix_timestamp(t)
{
  var dt = new Date(t*1000);
  var hr = dt.getHours();
  var m = "0" + dt.getMinutes();
  var s = "0" + dt.getSeconds();
  return hr+ ':' + m.substr(-2) + ':' + s.substr(-2);
}

function updateChat(place){
  axios.get('/chat/'+place, {withCredentials: true})
    .then(function (response) {
      let chat = $('#chat')
      let userlist = $('#userlist')
      let msgs = response.data.msgs
      let users = response.data.users
      userlist.empty()
      for (u in users){
        user = $("<p></p>").text(users[u])
        userlist.append(user);
      }

      chat.empty()
      for (m in msgs){
        time = $("<span></span>").text(unix_timestamp(msgs[m].time) + " - ")
        user = $("<span></span>").text("["+msgs[m].user+"] ")
        msg = $("<span></span>").text(msgs[m].msg)
        msgC = $("<p></p>").append(time, user, msg)
        chat.append(msgC);
      }
      if (goDown){
        chat.scrollTop(chat.prop("scrollHeight"));
        goDown = false;
      }

      // handle success
    })
    .catch(function (error) {
      // handle error
      console.log(error);
    })
    .then(function () {
      // always executed
    });
}

function sendMsg(place){
  let msgInput = $('#msg');
  let msgText = msgInput.val();
  msgInput.val("")
  if (msgText != ""){
    axios.post('/chat/msg/'+place, {'msg': msgText}, {withCredentials: true})
    .then(function (response) {
      goDown = true;
    })
    .catch(function (error) {
      console.log(error);
    });
   }
}
