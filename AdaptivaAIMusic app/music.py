< !DOCTYPE
html >
< html
lang = "en" >
< head >
< meta
charset = "UTF-8" >
< meta
name = "viewport"
content = "width=device-width, initial-scale=1.0" >
< title > Adaptive
Music
Recommendation
System < / title >
< style >
*{
    margin: 0;
padding: 0;
box - sizing: border - box;
}

body
{
    font - family: Arial, sans - serif;
background: linear - gradient(135
deg,  # 667eea 0%, #764ba2 100%);
min - height: 100
vh;
padding: 20
px;
color:  # 333;
}

.container
{
    max - width: 800px;
margin: 0
auto;
background: rgba(255, 255, 255, 0.95);
border - radius: 20
px;
padding: 30
px;
box - shadow: 0
15
px
35
px
rgba(0, 0, 0, 0.1);
}

h1
{
    text - align: center;
margin - bottom: 30
px;
color:  # 4a5568;
font - size: 2.5
em;
}

.stats - panel
{
    background:  # f7fafc;
        border - radius: 15
px;
padding: 20
px;
margin - bottom: 30
px;
border - left: 5
px
solid  # 667eea;
}

.stats - grid
{
    display: grid;
grid - template - columns: repeat(auto - fit, minmax(200
px, 1
fr));
gap: 20
px;
margin - bottom: 20
px;
}

.stat - item
{
    text - align: center;
padding: 15
px;
background: white;
border - radius: 10
px;
box - shadow: 0
2
px
10
px
rgba(0, 0, 0, 0.05);
}

.stat - value
{
    font - size: 2em;
font - weight: bold;
color:  # 667eea;
}

.stat - label
{
    color:  # 666;
        margin - top: 5
px;
}

.recommendation - section
{
    margin - bottom: 30px;
}

.section - title
{
    font - size: 1.5em;
margin - bottom: 20
px;
color:  # 4a5568;
border - bottom: 2
px
solid  # 667eea;
padding - bottom: 10
px;
}

.song - card
{
    background: white;
border - radius: 15
px;
padding: 20
px;
margin - bottom: 15
px;
box - shadow: 0
5
px
15
px
rgba(0, 0, 0, 0.08);
transition: all
0.3
s
ease;
border - left: 4
px
solid  # 667eea;
}

.song - card: hover
{
    transform: translateY(-2px);
box - shadow: 0
8
px
25
px
rgba(0, 0, 0, 0.12);
}

.song - header
{
    display: flex;
justify - content: space - between;
align - items: center;
margin - bottom: 15
px;
}

.song - info
{
    flex - grow: 1;
}

.song - title
{
    font - size: 1.2em;
font - weight: bold;
color:  # 2d3748;
margin - bottom: 5
px;
}

.song - artist
{
    color:  # 666;
        margin - bottom: 5
px;
}

.song - genre
{
    display: inline - block;
background:  # 667eea;
color: white;
padding: 3
px
8
px;
border - radius: 12
px;
font - size: 0.8
em;
}

.song - actions
{
    display: flex;
gap: 10
px;
margin - top: 15
px;
}

.btn
{
    padding: 8px 16px;
border: none;
border - radius: 20
px;
cursor: pointer;
font - size: 0.9
em;
transition: all
0.3
s
ease;
font - weight: 500;
}

.btn - like
{
    background:  # 48bb78;
        color: white;
}

.btn - like: hover
{
    background:  # 38a169;
        transform: scale(1.05);
}

.btn - dislike
{
    background:  # f56565;
        color: white;
}

.btn - dislike: hover
{
    background:  # e53e3e;
        transform: scale(1.05);
}

.btn - skip
{
    background:  # ed8936;
        color: white;
}

.btn - skip: hover
{
    background:  # dd6b20;
        transform: scale(1.05);
}

.btn - primary
{
    background:  # 667eea;
        color: white;
padding: 12
px
24
px;
font - size: 1.1
em;
display: block;
margin: 20
px
auto;
width: fit - content;
}

.btn - primary: hover
{
    background:  # 5a67d8;
        transform: scale(1.05);
}

.adaptation - log
{
    background:  # f0fff4;
        border - radius: 10
px;
padding: 15
px;
margin - top: 20
px;
border - left: 4
px
solid  # 48bb78;
}

.log - title
{
    font - weight: bold;
color:  # 2f855a;
margin - bottom: 10
px;
}

.log - item
{
    background: white;
padding: 10
px;
margin - bottom: 8
px;
border - radius: 8
px;
border - left: 3
px
solid  # 48bb78;
font - size: 0.9
em;
}

.preference - bars
{
    margin - top: 20px;
}

.preference - item
{
    margin - bottom: 15px;
}

.preference - label
{
    display: flex;
justify - content: space - between;
margin - bottom: 5
px;
font - weight: 500;
}

.preference - bar
{
    height: 8px;
background:  # e2e8f0;
border - radius: 4
px;
overflow: hidden;
}

.preference - fill
{
    height: 100 %;
background: linear - gradient(90
deg,  # 667eea, #764ba2);
transition: width
0.5
s
ease;
}

.updating
{
    animation: pulse 0.6s ease - in -out;
}

@keyframes


pulse
{
    0 % {transform: scale(1);}
50 % {transform: scale(1.05);}
100 % {transform: scale(1);}
}
< / style >
    < / head >
        < body >
        < div


class ="container" >

< h1 >🎵 Adaptive
Music
Recommender < / h1 >

< div


class ="stats-panel" >

< div


class ="stats-grid" >

< div


class ="stat-item" >

< div


class ="stat-value" id="totalInteractions" > 0 < / div >

< div


class ="stat-label" > Total Interactions < / div >

< / div >
< div


class ="stat-item" >

< div


class ="stat-value" id="likesCount" > 0 < / div >

< div


class ="stat-label" > Songs Liked < / div >

< / div >
< div


class ="stat-item" >

< div


class ="stat-value" id="topGenre" > - < / div >

< div


class ="stat-label" > Top Genre < / div >

< / div >
< div


class ="stat-item" >

< div


class ="stat-value" id="adaptationLevel" > Beginner < / div >

< div


class ="stat-label" > Learning Level < / div >

< / div >
< / div >

< div


class ="preference-bars" >

< div


class ="preference-item" >

< div


class ="preference-label" >

< span > Pop
Preference < / span >
< span
id = "popScore" > 0 % < / span >
< / div >
< div


class ="preference-bar" >

< div


class ="preference-fill" id="popFill" style="width: 0%;" > < / div >

< / div >
< / div >
< div


class ="preference-item" >

< div


class ="preference-label" >

< span > Rock
Preference < / span >
< span
id = "rockScore" > 0 % < / span >
< / div >
< div


class ="preference-bar" >

< div


class ="preference-fill" id="rockFill" style="width: 0%;" > < / div >

< / div >
< / div >
< div


class ="preference-item" >

< div


class ="preference-label" >

< span > Electronic
Preference < / span >
< span
id = "electronicScore" > 0 % < / span >
< / div >
< div


class ="preference-bar" >

< div


class ="preference-fill" id="electronicFill" style="width: 0%;" > < / div >

< / div >
< / div >
< div


class ="preference-item" >

< div


class ="preference-label" >

< span > Jazz
Preference < / span >
< span
id = "jazzScore" > 0 % < / span >
< / div >
< div


class ="preference-bar" >

< div


class ="preference-fill" id="jazzFill" style="width: 0%;" > < / div >

< / div >
< / div >
< / div >
< / div >

< div


class ="recommendation-section" >

< h2


class ="section-title" > 🎯 Personalized Recommendations < / h2 >

< div
id = "recommendations" > < / div >
< button


class ="btn btn-primary" onclick="generateRecommendations()" > Get New Recommendations < / button >

< / div >

< div


class ="adaptation-log" >

< div


class ="log-title" > 🧠 System Learning Log < / div >

< div
id = "adaptationLog" >
< div


class ="log-item" > System initialized.Ready to learn your preferences! < / div >

< / div >
< / div >
< / div >

< script >


class AdaptiveMusicSystem {
constructor() {
this.userPreferences = {
pop: 0,
rock: 0

,
electronic: 0,
jazz: 0
};

this.interactionHistory = [];
this.totalInteractions = 0;
this.likesCount = 0;

this.songDatabase = [
    {id: 1, title: "Starlight Dreams", artist: "Luna Echo", genre: "pop", energy: 0.8, danceability: 0.7},
    {id: 2, title: "Thunder Road", artist: "Electric Storm", genre: "rock", energy: 0.9, danceability: 0.6},
    {id: 3, title: "Midnight Pulse", artist: "Neon Nights", genre: "electronic", energy: 0.85, danceability: 0.9},
    {id: 4, title: "Smooth Saxophone", artist: "Blue Note Collective", genre: "jazz", energy: 0.4, danceability: 0.3},
    {id: 5, title: "Summer Breeze", artist: "Coastal Vibes", genre: "pop", energy: 0.6, danceability: 0.8},
    {id: 6, title: "Metal Heart", artist: "Iron Phoenix", genre: "rock", energy: 0.95, danceability: 0.4},
    {id: 7, title: "Digital Dreams", artist: "Cyber Pulse", genre: "electronic", energy: 0.7, danceability: 0.85},
    {id: 8, title: "Blue Monday", artist: "Jazz Fusion", genre: "jazz", energy: 0.5, danceability: 0.4},
    {id: 9, title: "Radio Waves", artist: "Pop Stars", genre: "pop", energy: 0.75, danceability: 0.75},
    {id: 10, title: "Guitar Hero", artist: "Rock Legends", genre: "rock", energy: 0.88, danceability: 0.5},
    {id: 11, title: "Bass Drop", artist: "EDM Masters", genre: "electronic", energy: 0.92, danceability: 0.95},
    {id: 12, title: "Mellow Mood", artist: "Smooth Jazz Trio", genre: "jazz", energy: 0.3, danceability: 0.2}
];

this.currentRecommendations = [];
this.recommendationWeights = {
    genrePreference: 0.6,
    energyMatch: 0.2,
    danceabilityMatch: 0.2
};

this.init();
}

init()
{
    this.generateRecommendations();
this.updateUI();
}

adaptToUserFeedback(songId, action)
{
    const
song = this.songDatabase.find(s= > s.id == = songId);
if (!song)
    return;

this.totalInteractions + +;

const
interaction = {
    timestamp: new Date(),
songId: songId,
action: action,
genre: song.genre,
energy: song.energy,
danceability: song.danceability
};

this.interactionHistory.push(interaction);

let
preferenceChange = 0;
let
logMessage = "";

switch(action)
{
    case
'like': \
    preferenceChange = 0.15;
this.likesCount + +;
logMessage = `Liked
"${song.title}"(${song.genre}) - Increased ${song.genre}
preference
by ${preferenceChange * 100} % `;
break;
case
'dislike':
preferenceChange = -0.1;
logMessage = `Disliked
"${song.title}"(${song.genre}) - Decreased ${song.genre}
preference
by ${Math.abs(preferenceChange) * 100} % `;
break;
case
'skip':
preferenceChange = -0.05;
logMessage = `Skipped
"${song.title}"(${song.genre}) - Slightly
decreased ${song.genre}
preference
`;
break;
}

this.userPreferences[song.genre] = Math.max(0, Math.min(1,
                                                        this.userPreferences[song.genre] + preferenceChange));

this.adaptRecommendationStrategy();
this.logAdaptation(logMessage);
this.updateUI();
this.triggerVisualFeedback();
}

adaptRecommendationStrategy()
{
    const
recentInteractions = this.interactionHistory.slice(-10);

const
likeRate = recentInteractions.filter(i= > i.action == = 'like').length / recentInteractions.length;
const
skipRate = recentInteractions.filter(i= > i.action == = 'skip').length / recentInteractions.length;

if (likeRate > 0.7)
{
this.logAdaptation("High satisfaction detected - maintaining current recommendation strategy");
} else if (skipRate > 0.6) {
this.recommendationWeights.genrePreference = Math.min(0.8, this.recommendationWeights.genrePreference + 0.1);
this.logAdaptation("High skip rate detected - increased genre preference weight to improve recommendations");
} else if (likeRate < 0.3) {
this.recommendationWeights.genrePreference = Math.max(0.4, this.recommendationWeights.genrePreference - 0.1);
this.logAdaptation("Low satisfaction detected - diversifying recommendations by reducing genre preference weight");
}
}

generateRecommendations()
{
    const
numRecommendations = 3;

const
scoredSongs = this.songDatabase.map(song= > ({
    ...song,
score: this.calculateRecommendationScore(song)
}));

scoredSongs.sort((a, b) = > b.score - a.score);
const
diverseRecommendations = this.ensureDiversity(scoredSongs, numRecommendations);

this.currentRecommendations = diverseRecommendations.slice(0, numRecommendations);
this.renderRecommendations();

this.logAdaptation(`Generated ${numRecommendations}
new
recommendations
based
on
current
preferences
`);
}

calculateRecommendationScore(song)
{
    const
genrePreference = this.userPreferences[song.genre] | | 0;

let
score = genrePreference * this.recommendationWeights.genrePreference;
score += song.energy * this.recommendationWeights.energyMatch;
score += song.danceability * this.recommendationWeights.danceabilityMatch;

if (this.totalInteractions < 5)
{
score += Math.random() * 0.3;
}

const
recentlyRecommended = this.interactionHistory.slice(-5).some(i= > i.songId == = song.id);
if (recentlyRecommended) {
score *= 0.5;
}

return score;
}

ensureDiversity(scoredSongs, count)
{
const
diverse = [];
const
genresUsed = new
Set();

for (const song of scoredSongs) {
if (diverse.length >= count)
    break;

if (!genresUsed.has(song.genre) | | genresUsed.size >= 4) {
diverse.push(song);
genresUsed.add(song.genre);
}
}

return diverse;
}

renderRecommendations()
{
const
container = document.getElementById('recommendations');
container.innerHTML = '';

this.currentRecommendations.forEach(song= > {
    const
songCard = document.createElement('div');
songCard.className = 'song-card';
songCard.innerHTML = `
                     < div


class ="song-header" >

< div


class ="song-info" >

< div


class ="song-title" > ${song.title} < / div >

< div


class ="song-artist" > by ${song.artist} < / div >

< span


class ="song-genre" > ${song.genre} < / span >

< / div >
< / div >
< div


class ="song-actions" >

< button


class ="btn btn-like" onclick="musicSystem.handleFeedback(${song.id}, 'like')" >

👍 Like
< / button >
< button


class ="btn btn-dislike" onclick="musicSystem.handleFeedback(${song.id}, 'dislike')" >

👎 Dislike
< / button >
< button


class ="btn btn-skip" onclick="musicSystem.handleFeedback(${song.id}, 'skip')" >

⏭️
Skip
< / button >
< / div >
`;
container.appendChild(songCard);
});
}

updateUI()
{
    document.getElementById('totalInteractions').textContent = this.totalInteractions;
document.getElementById('likesCount').textContent = this.likesCount;

const
topGenre = Object.entries(this.userPreferences)
.reduce((a, b) = > a[1] > b[1] ? a: b)[0];
document.getElementById('topGenre').textContent =
this.userPreferences[topGenre] > 0 ? topGenre: '-';

const
adaptationLevel = this.getAdaptationLevel();
document.getElementById('adaptationLevel').textContent = adaptationLevel;

Object.entries(this.userPreferences).forEach(([genre, value]) = > {
const
percentage = Math.round(value * 100);
document.getElementById(`${genre}
Score
`).textContent = `${percentage} % `;
document.getElementById(`${genre}
Fill
`).style.width = `${percentage} % `;
});
}

getAdaptationLevel()
{
if (this.totalInteractions < 5)
return 'Beginner';
if (this.totalInteractions < 15) return 'Learning';
if (this.totalInteractions < 30) return 'Adapting';
return 'Expert';
}

handleFeedback(songId, action)
{
this.adaptToUserFeedback(songId, action);

const
songCards = document.querySelectorAll('.song-card');
songCards.forEach(card= > {
    const
buttons = card.querySelectorAll('button');
buttons.forEach(button= > {
if (button.onclick & & button.onclick.toString().includes(songId))
{
    card.style.opacity = '0.5';
card.style.pointerEvents = 'none';
}
});
});
}

logAdaptation(message)
{
const
logContainer = document.getElementById('adaptationLog');
const
logItem = document.createElement('div');
logItem.className = 'log-item';
logItem.textContent = `${new
Date().toLocaleTimeString()}: ${message}
`;
logContainer.appendChild(logItem);

while (logContainer.children.length > 10) {
logContainer.removeChild(logContainer.firstChild);
}

logContainer.scrollTop = logContainer.scrollHeight;
}

triggerVisualFeedback()
{
const
statsPanel = document.querySelector('.stats-panel');
statsPanel.classList.add('updating');
setTimeout(() = > {
    statsPanel.classList.remove('updating');
}, 600);
}
}

const
musicSystem = new
AdaptiveMusicSystem();

function
generateRecommendations()
{
    musicSystem.generateRecommendations();
}

console.log('Adaptive Music Recommendation System initialized');
< / script >
    < / body >
        < / html >