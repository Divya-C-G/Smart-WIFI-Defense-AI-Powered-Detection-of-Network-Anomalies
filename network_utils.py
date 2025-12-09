import psutil
import socket
import ipaddress
import random
from datetime import datetime
import requests
import pandas as pd
import streamlit as st

def is_private_ip(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except Exception:
        return False

def get_ip_geolocation(ip):
    if not ip or ip == "127.0.0.1":
        return "Localhost"
    if is_private_ip(ip):
        return "Private Network"
    try:
        # keep timeout short so UI doesn't hang
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=2)
        if response.status_code == 200:
            data = response.json()
            city = data.get("city", "")
            region = data.get("region", "")
            country = data.get("country", "")
            loc_str = ", ".join(filter(None, [city, region, country]))
            return loc_str if loc_str else "Unknown"
    except requests.RequestException:
        return "Unknown"
    return "Unknown"

def extract_protocol_stats():
    # Placeholder for protocol extraction - keep simple for now
    protocols = ["TCP", "UDP", "ICMP", "OTHER"]
    return random.choice(protocols)

def get_multi_iface_stats(selected_ifaces):
    """
    Returns a DataFrame with per-interval (delta) bytes_sent / bytes_recv.
    Uses st.session_state.prev_counters to compute deltas between calls.
    """
    if "prev_counters" not in st.session_state:
        st.session_state.prev_counters = {}

    net_io = psutil.net_io_counters(pernic=True)
    addrs = psutil.net_if_addrs()
    data = []
    now = datetime.now()

    for iface in selected_ifaces:
        stats = net_io.get(iface)
        iface_addrs = addrs.get(iface, [])
        ip = None
        for addr in iface_addrs:
            if addr.family == socket.AF_INET:
                ip = addr.address
                break

        location = get_ip_geolocation(ip) if ip else "Unknown"
        protocol = extract_protocol_stats()

        # If stats is None, skip (interface may be down or nonexistent this moment)
        if not stats:
            continue

        # Compute deltas vs previous snapshot (prev counters are cumulative since boot)
        prev = st.session_state.prev_counters.get(iface)
        if prev:
            delta_sent = stats.bytes_sent - prev.get("bytes_sent", stats.bytes_sent)
            delta_recv = stats.bytes_recv - prev.get("bytes_recv", stats.bytes_recv)
            # delta may be negative if counters reset (e.g., interface restarted) -> clamp to 0
            if delta_sent < 0:
                delta_sent = 0
            if delta_recv < 0:
                delta_recv = 0
        else:
            # first reading: cannot compute delta, set to 0 to avoid misleading spikes
            delta_sent = 0
            delta_recv = 0

        # Save current cumulative counters for next iteration
        st.session_state.prev_counters[iface] = {
            "bytes_sent": stats.bytes_sent,
            "bytes_recv": stats.bytes_recv,
            "timestamp": now
        }

        data.append({
            "timestamp": now,
            "interface": iface,
            "ip_address": ip if ip else "N/A",
            "location": location,
            # store per-interval bytes (deltas), but also keep cumulative if desired
            "bytes_sent": int(delta_sent),
            "bytes_recv": int(delta_recv),
            "cum_bytes_sent": int(stats.bytes_sent),
            "cum_bytes_recv": int(stats.bytes_recv),
            "protocol": protocol
        })

    return pd.DataFrame(data)
