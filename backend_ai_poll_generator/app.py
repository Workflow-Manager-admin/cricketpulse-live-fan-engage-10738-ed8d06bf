import os
import random
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# -----------------------------
# Simulated Live Commentary Feed
# -----------------------------
COMMENTARY_FEED = [
    "Ball 6.1: OUT! Bowled! The batsman completely misses the yorker.",
    "Ball 8.3: SIX! He launches it over long-leg for a huge six!",
    "Ball 10.4: FOUR! Clever reverse-sweep, races to the boundary.",
    "Ball 13.2: WICKET! LBW appeal, umpire gives it out after review.",
    "Ball 15.5: Fifty up for the batsman, crowd cheers loudly!",
    "Ball 18.6: Massive six over midwicket, changing game momentum!",
    "Ball 20.0: It's the end of the innings, what a finish!"
]
COMMENTARY_INDEX = [0]  # Mutable wrapper to simulate 'live' updates

def get_live_commentary():
    """Simulate fetching the next update from live commentary."""
    idx = COMMENTARY_INDEX[0]
    if idx < len(COMMENTARY_FEED):
        commentary = COMMENTARY_FEED[idx]
        COMMENTARY_INDEX[0] += 1
        return commentary
    else:
        # No more fresh commentary; simulate as static
        return random.choice(COMMENTARY_FEED)

# --------------------------
# Poll and Voting Structures
# --------------------------
class Poll:
    def __init__(self, question, options):
        self.id = random.randint(1000, 9999)
        self.question = question
        self.options = options  # List of strings
        self.votes = [0 for _ in options]

    def to_dict(self, include_votes=False):
        data = {
            "id": self.id,
            "question": self.question,
            "options": self.options
        }
        if include_votes:
            data["votes"] = self.votes
        return data

# In-memory data store for demo (not persistent)
CURRENT_POLLS = []
LAST_GENERATED_COMMENTARY = ""

# --------------------------
# AI Poll Generation (Simple)
# --------------------------
# PUBLIC_INTERFACE
def generate_poll_from_commentary(commentary):
    """AI-inspired (but rule-based here) logic for creating an interesting fan poll from commentary."""
    # For demonstration, use keyword-based template polls:
    if "OUT" in commentary or "WICKET" in commentary:
        question = "Who will be the next batsman to get out?"
        options = ["Player A", "Player B", "Player C", "No wicket next over"]
    elif "SIX" in commentary or "four" in commentary.upper():
        question = "How many runs will be scored in the current over?"
        options = ["0-3", "4-8", "9-15", "More than 15"]
    elif "Fifty" in commentary or "fifty" in commentary:
        question = "Will the batsman reach a century?"
        options = ["Yes", "No"]
    elif "end of the innings" in commentary or "finish" in commentary:
        question = "Is the current total defendable?"
        options = ["Yes", "No", "Too Close to Call"]
    else:
        # General fallback poll
        question = "What will happen on the next ball?"
        options = ["Dot ball", "Single", "Boundary", "Wicket"]
    return Poll(question, options)

def maybe_generate_new_poll():
    """Generate a new poll if latest commentary line has changed."""
    global LAST_GENERATED_COMMENTARY
    commentary = get_live_commentary()
    if commentary != LAST_GENERATED_COMMENTARY:
        LAST_GENERATED_COMMENTARY = commentary
        new_poll = generate_poll_from_commentary(commentary)
        CURRENT_POLLS.append(new_poll)
        # Keep only the last 3 polls for demo purpose
        if len(CURRENT_POLLS) > 3:
            CURRENT_POLLS.pop(0)
        return new_poll
    return None

# --------------------------------
# REST API Endpoints
# --------------------------------

@app.route('/api/commentary', methods=['GET'])
def api_get_commentary():
    """
    Get the current/latest cricket commentary line. Simulates real-time commentary feed.
    ---
    responses:
      200:
        description: Current live commentary
    """
    commentary = get_live_commentary()
    return jsonify({"commentary": commentary})

@app.route('/api/polls', methods=['GET'])
def api_get_poll():
    """
    Get the latest AI-generated poll for fans to respond.
    ---
    responses:
      200:
        description: Latest poll details
    """
    maybe_generate_new_poll()
    if CURRENT_POLLS:
        poll = CURRENT_POLLS[-1]
        return jsonify({"poll": poll.to_dict()})
    else:
        return jsonify({"poll": None})

@app.route('/api/polls/<int:poll_id>/vote', methods=['POST'])
def api_vote_poll(poll_id):
    """
    Submit a vote for a given poll.
    ---
    parameters:
      - name: poll_id
        in: path
        description: Poll identifier
        required: True
        type: integer
      - name: option
        in: body
        description: Index of selected option
        required: True
        type: object
        schema:
          type: object
          properties:
            option:
              type: integer
    responses:
      200:
        description: Vote registered successfully
    """
    data = request.get_json()
    option = data.get("option")
    # Find poll
    poll = next((p for p in CURRENT_POLLS if p.id == poll_id), None)
    if poll and isinstance(option, int) and 0 <= option < len(poll.options):
        poll.votes[option] += 1
        return jsonify({"success": True, "poll_id": poll_id, "option": option})
    return jsonify({"success": False, "message": "Invalid poll or option"}), 400

@app.route('/api/polls/<int:poll_id>/results', methods=['GET'])
def api_poll_results(poll_id):
    """
    Get real-time aggregated results for a poll (vote counts).
    ---
    parameters:
      - name: poll_id
        in: path
        description: Poll identifier
        required: True
        type: integer
    responses:
      200:
        description: Poll results
    """
    poll = next((p for p in CURRENT_POLLS if p.id == poll_id), None)
    if poll is not None:
        return jsonify({"results": poll.to_dict(include_votes=True)})
    return jsonify({"results": None}), 404

@app.route('/', methods=['GET'])
def index():
    """Basic health check endpoint."""
    return jsonify({"service": "AI Poll Generator Backend", "status": "OK"})

# ---------------------------
# Entry point for app startup
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
