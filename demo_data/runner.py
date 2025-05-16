#!/usr/bin/env python
# Copyright 2025 NetBox Labs Inc
"""NetBox Labs - Mock Impl."""

from collections.abc import Iterable
from typing import Any
import json
import random
import string

from netboxlabs.diode.sdk.ingester import Device, Interface, Entity
from worker.backend import Backend
from worker.models import Metadata, Policy


class DemoData(Backend):

    def setup(self) -> Metadata:
        return Metadata(name="demo_data", app_name="demo_data_app", app_version="1.0.0")


    def run(self, policy_name: str, policy: Policy) -> Iterable[Entity]:
        
        p = json.loads(policy.model_dump_json())
        device_count = p.get('scope', {}).get('device_count')
        
        entities = []

        for i in range(max(1, min(2*device_count, round(random.gauss(device_count, 3))))):

            prefix = "".join(random.choice(["Switch","Router","Server"]))
            suffix = "".join(random.choice(["A","B","C"]))
            intf =  "".join(random.choice(["0","1","2"]))
            
            device = Device(
                name=f"{prefix} {suffix}",
                device_type=f"Device Type {suffix}",
                platform=f"Platform {suffix}",
                manufacturer=f"Manufacturer {suffix}",
                description="",
                comments="",
                site="Site ABC",
                role=f"Role {suffix}",
                serial="123456",
                asset_tag="ABCDEF",
                status="active"
            )
            entities.append(Entity(device=device))

            interface = Interface(
                name=f"Eth{intf}",
                device=Device(
                    name=f"{prefix} {suffix}",
                    manufacturer=f"Manufacturer {suffix}",
                    device_type=f"Device Type {suffix}",
                    role=f"Role {suffix}",
                    site="Site ABC"
                ),
                type="other",
                enabled=True,
                mtu=1500,
                mac_address=":".join(f"{random.randint(0, 255):02x}" for _ in range(6)),
                description="",
            )
            entities.append(Entity(interface=interface))

        return entities


    def generate_device_name(prefixes=None, length=4):
        if prefixes is None:
            prefixes = ["sw", "rtr", "fw", "lb", "ap", "srv"]
        suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
        return f"{random.choice(prefixes)}-{suffix}"