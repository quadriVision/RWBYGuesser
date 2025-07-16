import sqlite3
import os
import json
from flask import Flask, request, make_response, send_file, send_from_directory,jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
import random
import bleach
games = []
episodes = ['S1E1 - Ruby Rose', 'S1E2 - The Shining Beacon', 'S1E3 - The Shining Beacon, Pt.2', 'S1E4 - The First Step', 'S1E5 - The First Step, Pt.2', 'S1E6 - The Emerald Forest', 'S1E7 - The Emerald Forest, Pt.2', 'S1E8 - Players and Pieces', 'S1E9 - The Badge and The Burden', 'S1E10 - The Badge and The Burden, Pt.2', 'S1E11 - Jaunedice', 'S1E12 - Jaunedice, Pt.2', 'S1E13 - Forever Fall', 'S1E14 - Forever Fall, Pt.2', 'S1E15 - The Stray', 'S1E16 - Black and White', 'S2E1 - Best Day Ever', 'S2E2 - Welcome to Beacon', 'S2E3 - A Minor Hiccup', 'S2E4 - Painting the Town', 'S2E5 - Extracurricular', 'S2E6 - Burning the Candle', 'S2E7 - Dance Dance Infiltration', 'S2E8 - Field Trip', 'S2E9 - Search and Destroy', 'S2E10 - Mountain Glenn', 'S2E11 - No Brakes', 'S2E12 - Breach', 'S3E1 - Round One', 'S3E2 - New Challengers', "S3E3 - It's Brawl in the Family", 'S3E4 - Lessons Learned', 'S3E5 - Never Miss a Beat', 'S3E6 - Fall', 'S3E7 - Beginning of the End', 'S3E8 - Destiny', 'S3E9 - PvP', 'S3E10 - Battle of Beacon', 'S3E11 - Heroes and Monsters', 'S3E12 - End of the Beginning', 'SE - Volume 4 Character Short', 'S4E1 - The Next Step', 'S4E2 - Remembrance', 'S4E3 - Of Runaways and Stowaways', 'S4E4 - Family', 'S4E5 - Menagerie', 'S4E6 - Tipping Point', 'S4E7 - Punished', 'S4E8 - A Much Needed Talk', 'S4E9 - Two Steps Forward, Two Steps Back', 'S4E10 - Kuroyuri', 'S4E11 - Taking Control', 'S4E12 - No Safe Haven', 'SE - Volume 5 Weiss Character Short', 'SE - Volume 5 Blake Character Short', 'SE - Volume 5 Yang Character Short', 'S5E1 - Welcome to Haven', 'S5E2 - Dread in the Air', 'S5E3 - Unforeseen Complications', 'S5E4 - Lighting the Fire', 'S5E5 - Necessary Sacrifice', 'S5E6 - Known by its Song', 'S5E7 - Rest and Resolutions', 'S5E8 - Alone Together', 'S5E9 - A Perfect Storm', 'S5E10 - True Colors', 'S5E11 - The More the Merrier', 'S5E12 - Vault of the Spring Maiden', 'S5E13 - Downfall', "S5E14 - Haven's Fate", 'SE - Volume 6 Adam Character Short', 'S6E1 - Argus Limited', 'S6E2 - Uncovered', 'S6E3 - The Lost Fable', "S6E4 - So That's How It Is", 'S6E5 - The Coming Storm', 'S6E6 - Alone in the Woods', 'S6E7 - The Grimm Reaper', 'S6E8 - Dead End', 'S6E9 - Lost', 'S6E10 - Stealing from the Elderly', 'S6E11 - The Lady in the Shoe', 'S6E12 - Seeing Red', 'S6E13 - Our Way', 'S7E1 - The Greatest Kingdom', 'S7E2 - A New Approach', 'S7E3 - Ace Operatives', 'S7E4 - Pomp and Circumstance', 'S7E5 - Sparks', 'S7E6 - A Night Off', 'S7E7 - Worst Case Scenario', 'S7E8 - Cordially Invited', 'S7E9 - As Above, So Below', 'S7E10 - Out in the Open', 'S7E11 - Gravity', 'S7E12 - With Friends Like These', 'S7E13 - The Enemy of Trust', 'S8E1 - Divide', 'S8E2 - Refuge', 'S8E3 - Strings', 'S8E4 - Fault', 'S8E5 - Amity', 'S8E6 - Midnight', 'S8E7 - War', 'S8E8 - Dark', 'S8E9 - Witch', 'S8E10 - Ultimatum', 'S8E11 - Risk', 'S8E12 - Creation', 'S8E13 - Worthy', 'S8E14 - The Final Word', 'S9E1 - A Place of Particular Concern', 'S9E2 - Altercation at the Auspicious Auction', 'S9E3 - Rude, Red, and Royal', 'S9E4 - A Cat Most Curious', 'S9E5 - The Parfait Predicament', 'S9E6 - Confessions Within Cumulonimbus Clouds', 'S9E7 - The Perils of Paper Houses', 'S9E8 - Tea Amidst Terrible Trouble', 'S9E9 - A Tale Involving a Tree', 'S9E10 - Of Solitude and Self']
episodes_chibi = ['S1E1 - Ruby Makes Cookies', 'S1E2 - Cat Burglar', 'S1E3 - Reloading', 'S1E4 - Fighting Game', 'S1E5 - Sissy Fight', 'S1E6 - The Vacuum', 'S1E7 - Prank Wars', 'S1E8 - Magnetic Personality', 'S1E9 - Ren Plays Tag', 'S1E10 - Love Triangle', 'S1E11 - Nurse Ruby', 'S1E12 - Little Red Riding Hood', 'S1E13 - Spin the Bottle', 'S1E14 - Big Vacation', 'S1E15 - Neptune_s Phobia', 'S1E16 - Bike Race', 'S1E17 - Save Nora_', 'S1E18 - Evil Plans', 'S1E19 - Pillow Fight', 'S1E20 - Roman_s Revenge', 'S1E21 - Cinder Who_', 'S1E22 - Security Woes', 'S1E23 - A Slip Through Time and Space', 'S1E24 - The One with a Laugh Track', 'S2E1 - Director Ozpin', 'S2E2 - Geist Buster', 'S2E3 - Magic Show', 'S2E4 - Dad Jokes', 'S2E5 - Girls Rock_', 'S2E6 - Super Besties', 'S2E7 - Must Be Nice', 'S2E8 - Boy Band', 'S2E9 - Coming Home to Roost', 'S2E10 - Cool Dad', 'S2E11 - Movie Night', 'S2E12 - Evil Genius', 'S2E13 - Parent Teacher Conference', 'S2E14 - Cannonball_', 'S2E15 - Nurse Nora', 'S2E16 - Neptune Noir', 'S2E17 - The Mystery Bunch', 'S2E18 - The Fixer', 'S2E19 - Steals and Wheels', 'S2E20 - Monsters of Rock', 'S2E21 - Happy BirthdayWeen', 'S2E22 - Battle of the Bands', 'S2E23 - A Slip Through Time and Space Pt. 2', 'S2E24 - Nondescript Holiday Spectacular', 'S3E1 - Road Trip', 'S3E2 - Evil Interview', 'S3E3 - Mortal Frenemies', 'S3E4 - Grimm Passengers', 'S3E5 - Girls_ Night Out', 'S3E6 - Teenage Faunus Ninja Catgirl', 'S3E7 - Mysterious Red Button', 'S3E8 - Kids vs Adults vs Pups', 'S3E9 - Tea Party', 'S3E10 - Prank War', 'S3E11 - In The Clutches of Evil', 'S3E12 - JNPR Dreams', 'S3E13 - Cousins of Chaos', 'S3E14 - Nefarious Dreams', 'S3E15 - Play With Penny', 'S3E16 - RWBY Dreams', 'S4E1 - Cool as Coco', 'S4E2 - Love Life', 'S4E3 - Tai the Sub', 'S4E4 - True Blue Friend', 'S4E5 - Cardin_s Club', 'S4E6 - Master Thief', 'S4E7 - He Does It All', 'S4E8 - Behind the Scenes', 'S4E9 - Bad Criminal', 'S4E10 - Port_s Fort']
class Game:
    def __init__(self, lives, mode, username, timelimit = 0):
        self.game_id = random.randint(10_000_000,99_999_999)
        self.lives = lives
        self.original_lives = lives
        self.point = 0
        self.mode = mode
        self.name = username
        self.timelimit = timelimit
        self.lastsubmission = 0
        # current round
        self.episode = 0 # 0-999 main show, >1000 rwby chibi
    def setName(self, name):
        self.name = name
    def addPoint(self):
        self.point = self.point + 1
    def removeLive(self):
        self.lives = self.lives - 1
    def json_format(self):
        return {"Game ID": self.game_id, "Lives": self.lives, "Total lives": self.original_lives, "Point": self.point, "User": self.name, "Gamemode": self.mode}
    def __str__(self):
        return f"Game ID : {self.game_id} | Lives : {self.lives}/{self.original_lives} | Point : {self.point} | User : {self.name} | Gamemode : {self.mode}"

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

# serve static files
@app.route("/")
def index():
    return send_file("./index.html",mimetype='text/html')

@app.route("/leaderboard")
def leaderboard():
    return send_file("./leaderboard.html",mimetype='text/html')

# we create a new game from the username, gamemode and lives settings and return the game_id
@app.route("/api/start", methods=["POST"])
def start():
    username = request.json.get("username")
    gamemode = request.json.get('mode')
    if gamemode != "main" and gamemode != "chibi" and gamemode != "mainchibi":
        return make_response("wrong mode", 400)
    game = Game(request.json.get('lives'), gamemode, bleach.clean(username))
    games.append(game)
    resp = make_response(str(game.game_id), 200)
    resp.set_cookie("game_id", str(game.game_id))
    return resp

@app.route("/api/round", methods=["GET", "POST"])
def get_image():
    if request.method == "GET":
        # serve the latest round's image
        game_id = request.cookies.get('game_id')
        game = get_game(game_id)
        print(game)
        if not game:
            return make_response(f"invalid game_id : {str(game_id)}",400)
        else:
            if game.episode == 0:
                # get random image from random episode and return the image
                if game.mode == "main":
                    episode = random.randint(1,121)
                elif game.mode == "chibi":
                    episode = random.randint(1001,1074)
                else:
                    chibiormain = random.randint(0,1)
                    if chibiormain == 1:
                        episode = random.randint(1001,1074)
                    else:
                        episode = random.randint(1,121)
                game.episode = episode
                if episode < 1000:
                    image = random.choice(os.listdir(f"./episodes/{episodes[episode-1]}"))
                    print(f"Game ID : {game.game_id} || Showing episode id {episode} || Episode name : {episodes[episode-1]} || Points : {game.point} || Lives : {game.lives}")
                    resp = make_response(send_from_directory(f"./episodes/{episodes[episode-1]}", image))
                else:
                    image = random.choice(os.listdir(f"./episodes/Chibi{episodes_chibi[episode-1-1000]}"))
                    print(f"Game ID : {game.game_id} || Showing episode id {episode} || Episode name : {episodes_chibi[episode-1-1000]} || Points : {game.point} || Lives : {game.lives}")
                    resp = make_response(send_from_directory(f"./episodes/Chibi{episodes_chibi[episode-1-1000]}", image))
                resp.headers['X-Lives'] = str(game.lives)
                resp.headers['X-Points'] = str(game.point)
                resp.headers['Cache-Control'] = 'no-cache'
                return resp
            else:
                # game resumed, show an image from the last episode that was shown
                if game.episode < 1000:
                    image = random.choice(os.listdir(f"./episodes/{episodes[game.episode-1]}"))
                    print(f"Game ID : {game.game_id} || Showing episode id {game.episode} || Episode name : {episodes[game.episode-1]} || Points : {game.point} || Lives : {game.lives}")
                    resp = make_response(send_from_directory(f"./episodes/{episodes[game.episode-1]}", image))
                else:
                    image = random.choice(os.listdir(f"./episodes/Chibi{episodes_chibi[game.episode-1-1000]}"))
                    print(f"Game ID : {game.game_id} || Showing episode id {game.episode} || Episode name : {episodes_chibi[game.episode-1-1000]} || Points : {game.point} || Lives : {game.lives}")
                    resp = make_response(send_from_directory(f"./episodes/Chibi{episodes_chibi[game.episode-1-1000]}", image))
                resp.headers['X-Lives'] = str(game.lives)
                resp.headers['X-Points'] = str(game.point)
                resp.headers['Cache-Control'] = 'no-cache'
                return resp
    else:
        # handles the score submissions
        episode = request.json.get("episode")
        game_id = request.cookies.get('game_id')
        game = get_game(game_id)
        if game == False:
            return make_response("invalid game_id",400)
        if game.episode == episode:
            # correct guess
            game.addPoint()
            game.episode = 0
            resp = make_response("correct",200)
            resp.headers['X-Lives'] = str(game.lives)
            return resp
        else:
            # incorrect guess
            game.removeLive()
            if game.lives == 0:
                # game over, removes the game_id from the list of active games and writes the score to the database
                resp = make_response(str(game.episode),406)
                resp.headers['X-Points'] = str(game.point)
                resp.headers['X-Lives'] = str(game.lives)
                try:
                    print(f"User {game.name} just lost at {game.point} points!")
                    conn = sqlite3.connect('games.db')
                    cursor = conn.cursor()
                    sql_command = '''INSERT INTO {gamemode} (name,points,lives) VALUES(?,?,?)'''.format(gamemode=game.mode)
                    conn.execute(sql_command, (game.name, game.point, game.original_lives))
                    conn.commit()
                    """with open('./all_games.txt','a+') as gamelog:
                        gamelog.write(f"Game ID : {game.game_id} || Points : {game.point} || Lives : {game.original_lives}\n")"""
                except Exception as e:
                    print(e)
                games.remove(game)
                return resp
            else:
                resp = make_response(str(game.episode),420)
                resp.headers['X-Lives'] = str(game.lives)
                game.episode = 0
                return resp
        
# gets the top players from the database
@app.route("/api/leaderboard")
def fetch_leaderboard():
    try:
        conn = sqlite3.connect('games.db')
        lives = request.args["lives"]
        if lives != "0" and lives != "1" and lives != "3" and lives != "5":
            return make_response("Invalid lives", 400)
        gamemode = request.args["gamemode"]
        if gamemode != "main" and gamemode != "chibi" and gamemode != "mainchibi":
            return make_response("Invalid gamemode",400)
        offset = request.args["offset"]
        if lives == "0":
            sql_statement = f"SELECT * FROM {gamemode} ORDER BY points DESC LIMIT ?,10"
            info = conn.execute(sql_statement, (offset))
        else:
            sql_statement = f"SELECT * FROM {gamemode} WHERE lives = ? ORDER BY points DESC LIMIT ?,10"
            info = conn.execute(sql_statement, (lives, offset))
        return make_response(info.fetchall(), 200)
    except Exception as e:
        return make_response(str(e), 400)

# super secret logs :o resets on every restart
@app.route("/a1b2c3d4fatchibinora")
def get_logs():
    jsonned = []
    for game in games:
        jsonned.append(game.json_format())
    string = ""
    for jsonneddd in jsonned:
        string += json.dumps(jsonneddd) + "<br>"
    return make_response(f"{string}<br>Length : {len(games)}")


# ignore this, i never used it
@app.route("/api/end/<game_id>")
def stop(game_id):
    print(games)
    for game in games:
        try:
            if (game.game_id == int(game_id)):
                print("found")
                games.remove(game)
                resp = make_response("deleted", 200)
                return resp
        except:
            resp = make_response("szart küldtél ez mi a fasz???", 400)
            return resp
    resp = make_response("no matching game_id", 400)
    return resp

def get_game(game_id):
    for game in games:
        if (game.game_id == int(game_id)):
            return game
    return False

# serves a rwby screenshot as preview image for twitter
@app.route("/get_image")
def a():
    resp = make_response(send_from_directory(f"./", "1.webp"))
    return resp