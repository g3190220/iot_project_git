// JavaScript Document

var d = new Date();
const months = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
]
const days = [
  'Sun',
  'Mon',
  'Tue',
  'Wed',
  'Thu',
  'Fri',
  'Sat'
]
const dayIndex = d.getDay()
const dayName = days[dayIndex]

const date = d.getDate()

const monthIndex = d.getMonth()
const monthName = months[monthIndex]

const time=d.getHours()+":"+d.getMinutes()
document.getElementById("demo").innerHTML = monthName+" "+date+" "+dayName;
document.getElementById("demo2").innerHTML = time;

