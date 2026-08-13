#!/bin/sh
input=$(cat)
cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // "unknown"')
model=$(echo "$input" | jq -r '.model.display_name // "Claude"')
used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')

user=$(whoami)
host=$(hostname -s)

home="$HOME"
if [ "$cwd" = "$home" ]; then
  dir="~"
elif [ "${cwd#$home/}" != "$cwd" ]; then
  remainder="${cwd#$home/}"
  case "$remainder" in
    */*) dir=$(basename "$cwd") ;;
    *)   dir="~/$remainder" ;;
  esac
else
  dir=$(basename "$cwd")
fi

# ANSI colors
GRAY=$(printf '\033[90m')
YELLOW=$(printf '\033[33m')
RED=$(printf '\033[31m')
RESET=$(printf '\033[0m')

# Context usage with color
ctx=""
if [ -n "$used" ]; then
  used_int=$(printf "%.0f" "$used")
  if [ "$used_int" -ge 70 ]; then
    color="$RED"
  elif [ "$used_int" -ge 50 ]; then
    color="$YELLOW"
  else
    color="$GRAY"
  fi
  ctx=" | контекст: ${color}${used_int}%${RESET}"
fi

# Helper: format seconds into "Xд Yч" or "Yч Zм"
format_time() {
  local diff="$1"
  if [ "$diff" -le 0 ]; then
    echo ""
    return
  fi
  local days=$(( diff / 86400 ))
  local hours=$(( (diff % 86400) / 3600 ))
  local mins=$(( (diff % 3600) / 60 ))
  if [ "$days" -gt 0 ]; then
    echo "${days}д ${hours}ч"
  elif [ "$hours" -gt 0 ]; then
    echo "${hours}ч ${mins}м"
  else
    echo "${mins}м"
  fi
}

now=$(date +%s)

# 5-hour limit
five_pct=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
five_resets=$(echo "$input" | jq -r '.rate_limits.five_hour.resets_at // empty')
five_str=""
if [ -n "$five_pct" ]; then
  five_int=$(printf "%.0f" "$five_pct")
  five_str="5ч: ${five_int}%"
  if [ -n "$five_resets" ]; then
    five_diff=$(( five_resets - now ))
    five_time=$(format_time "$five_diff")
    [ -n "$five_time" ] && five_str="${five_str} (сброс ${five_time})"
  fi
fi

# 7-day limit
seven_pct=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')
seven_resets=$(echo "$input" | jq -r '.rate_limits.seven_day.resets_at // empty')
seven_str=""
if [ -n "$seven_pct" ]; then
  seven_int=$(printf "%.0f" "$seven_pct")
  seven_str="7д: ${seven_int}%"
  if [ -n "$seven_resets" ]; then
    seven_diff=$(( seven_resets - now ))
    seven_time=$(format_time "$seven_diff")
    [ -n "$seven_time" ] && seven_str="${seven_str} (сброс ${seven_time})"
  fi
fi

# Combine limits
limits=""
if [ -n "$five_str" ] && [ -n "$seven_str" ]; then
  limits=" | ${five_str} | ${seven_str}"
elif [ -n "$five_str" ]; then
  limits=" | ${five_str}"
elif [ -n "$seven_str" ]; then
  limits=" | ${seven_str}"
fi

printf "%s@%s %s | %s%s%s%s" "$user" "$host" "$dir" "${RED}${model}${RESET}" "$ctx" "$limits"
