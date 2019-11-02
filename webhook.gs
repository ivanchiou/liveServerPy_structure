var channelToken = 'your channel token';
var groupId = 'your groupid';
var userId = 'your userid';

function doPost(e) {
  var decoded = decodeURIComponent(e.postData.contents);
  decoded = decoded.replace('payload=','');
  var data = JSON.parse(decoded);
  try{
    var msg =getMsg(data);
    //Logger.log(JSON.stringify(data));
    pushMsg(channelToken, msg, userId);
    pushMsg(channelToken, msg, groupId);
    return ContentService.createTextOutput(msg);
  }
  catch(ex){
    Logger.log(ex);
    return ContentService.createTextOutput(ex);
  }
}

// 發送訊息
function pushMsg(channelToken, message, usrId) {
  var url = 'https://api.line.me/v2/bot/message/push';
  var opt = {
    'headers': {
      'Content-Type': 'application/json; charset=UTF-8',
      'Authorization': 'Bearer ' + channelToken,
    },
    'method': 'post',
    'payload': JSON.stringify({
      'to': usrId,
      'messages': [{'type': 'text', 'text': message}]
    })
  };
  UrlFetchApp.fetch(url, opt);
}

function getMsg(data){
  var repository_slug = data.repository.name;
  var result = data.result;
  var build_url = data.build_url;
  var build_number = data.number;
  var compare_url = data.compare_url;
  var commit = data.commit;
  var branch = data.branch;
  var message = data.message;
  var commiter = data.committer_name;
  var state = data.state;
  var type = data.type;
  var duration = data.duration;
  var ret = "";

  ret += "State: "+state+"\n";
  ret += "Type: "+type+"\n";
  ret += "Commiter: "+commiter.replace("+"," ")+"\n";
  ret += "Repo: "+repository_slug+"\n";
  ret += "Commit Message: "+message.replace("+"," ")+"\n";
  ret += "Execution time: "+duration+"s";
  //ret += "Compare: "+compare_url;
  return ret;
}
