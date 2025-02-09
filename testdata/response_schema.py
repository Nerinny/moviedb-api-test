TOP_RATED_MOVIES_SCHEMA = {
  "type": "object",
  "properties": {
    "page": {"type": "integer"},
    "total_results": {"type": "integer"},
    "total_pages": {"type": "integer"},
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "title": {"type": "string"},
          "overview": {"type": "string"},
          "release_date": {"type": "string", "format": "date"},
          "vote_average": {"type": "number"},
          "poster_path": {"type": "string"},
          "backdrop_path": {"type": "string"}
        },
      }
    }
  },
}


RATE_MOVIE_SCHEMA = {
  "type": "object",
  "properties": {
    "status_code": {
      "type": "integer"
    },
    "status_message": {
      "type": "string",
    }
  }
}