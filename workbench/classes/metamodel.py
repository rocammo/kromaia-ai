from .vector3 import Vector3
from .quaternion import Quaternion

''' ### AGGREGATION (5) ###

    * Hull       [1]
    * Weapon     [2]
    * Link       [3]
    * AIUnit     [4]
    * MovementAI [5]
'''


class Hull(object):
    def __init__(self, hull_type    : int,
                 scale              : Vector3, position              : Vector3, orientation              : Quaternion,
                 object_mass        : float,   object_material       : int,
                 object_maximum_life: float,   object_armor          : float,
                 destruction_delay  : float,   effect_multiplier_kill: float,   effect_multiplier_destroy: float,
                 effects_mask_kill  : str,     effects_mask_destroy  : str,
                 hull_index_parent  : int,     local_direction       : Vector3):
        self.hull_type = hull_type

        # ObjectData
        self.scale       = scale
        self.position    = position
        self.orientation = orientation

        # PhysicalObjectData
        self.object_mass     = float(object_mass)
        self.object_material = int(object_material)

        # AliveObjectData
        self.object_maximum_life       = float(object_maximum_life)
        self.object_armor              = float(object_armor)
        self.destruction_delay         = float(destruction_delay)
        self.effect_multiplier_kill    = float(effect_multiplier_kill)
        self.effect_multiplier_destroy = float(effect_multiplier_destroy)
        self.effects_mask_kill         = effects_mask_kill
        self.effects_mask_destroy      = effects_mask_destroy

        # ComponentData
        self.hull_index_parent = int(hull_index_parent)
        self.local_direction   = local_direction


class Weapon(object):
    def __init__(self, weapon_type  : int,
                 scale              : Vector3, position              : Vector3, orientation              : Quaternion,
                 object_mass        : float,   object_material       : int,
                 object_maximum_life: float,   object_armor          : float,
                 destruction_delay  : float,   effect_multiplier_kill: float,   effect_multiplier_destroy: float,
                 effects_mask_kill  : str,     effects_mask_destroy  : str,
                 hull_index_parent  : int,     local_direction       : Vector3,
                 weapon_priority    : int,     weapon_behaviour      : int,
                 reload_time        : float,   has_lock              : int,
                 affector_type      : int,     affector_scale_factor : float,   affector_power_factor    : float,
                 affector_position  : Vector3):
        self.weapon_type = weapon_type

        # ObjectData
        self.scale       = scale
        self.position    = position
        self.orientation = orientation

        # PhysicalObjectData
        self.object_mass     = float(object_mass)
        self.object_material = int(object_material)

        # AliveObjectData
        self.object_maximum_life       = float(object_maximum_life)
        self.object_armor              = float(object_armor)
        self.destruction_delay         = float(destruction_delay)
        self.effect_multiplier_kill    = float(effect_multiplier_kill)
        self.effect_multiplier_destroy = float(effect_multiplier_destroy)
        self.effects_mask_kill         = effects_mask_kill
        self.effects_mask_destroy      = effects_mask_destroy

        # ComponentData
        self.hull_index_parent = int(hull_index_parent)
        self.local_direction   = local_direction

        # WeaponData
        self.weapon_priority = int(weapon_priority)
        self.weapon_behaviour = int(weapon_behaviour)
        self.reload_time = float(reload_time)
        self.has_lock = int(has_lock)
        self.affector_type = int(affector_type)
        self.affector_scale_factor = float(affector_scale_factor)
        self.affector_power_factor = float(affector_power_factor)
        self.affector_position = affector_position


class Link(object):
    def __init__(self, link_type: int, hull_index_first: int, hull_index_second: int,
                 destructible          : int,   destruction_delay        : float,
                 effect_multiplier_kill: float, effect_multiplier_destroy: float,
                 effects_mask_kill     : str,   effects_mask_destroy     : str) :
        self.link_type = int(link_type)

        # LinkData
        self.hull_index_first          = int(hull_index_first)
        self.hull_index_second         = int(hull_index_second)
        self.destructible              = int(destructible)
        self.destruction_delay         = float(destruction_delay)
        self.effect_multiplier_kill    = float(effect_multiplier_kill)
        self.effect_multiplier_destroy = float(effect_multiplier_destroy)
        self.effects_mask_kill         = effects_mask_kill
        self.effects_mask_destroy      = effects_mask_destroy


''' ### ASSOCIATION (4) ###

    * Link-HullIndexFirst-Hull  [1]
    * Link-HullIndexSecond-Hull [2]
    * Weapon-MobileObject       [3]
    * Weapon-Cannon             [4]
'''


class MobileObject(object):
    def __init__(self, mobility_type: int, local_position: Vector3):
        self.mobility_type  = int(mobility_type)
        self.local_position = local_position

    def __repr__(self):
        return f"MobileObject(mobility_type: {self.mobility_type}, local_position: <{self.local_position}>)"


class WeaponWithMobileObjects(object):
    def __init__(self, scale: Vector3, position: Vector3, orientation: Quaternion,
                 hull_index_parent: int, local_direction: Vector3,
                 mobile_objects: list[MobileObject]):
        self.scale             = scale
        self.position          = position
        self.orientation       = orientation
        self.hull_index_parent = int(hull_index_parent)
        self.local_direction   = local_direction
        self.mobile_objects    = mobile_objects


class Cannon(object):
    def __init__(self, firing_turn_maximum: int, firing_turn_start: int, firing_turn_end: int,
                 roll: float, firing_position: Vector3, firing_direction: Vector3):
        self.firing_turn_maximum = int(firing_turn_maximum)
        self.firing_turn_start   = int(firing_turn_start)
        self.firing_turn_end     = int(firing_turn_end)
        self.roll                = float(roll)
        self.firing_position     = firing_position
        self.firing_direction    = firing_direction

    def __repr__(self):
        return f"Cannon(firing_turn_maximum: {self.firing_turn_maximum}, firing_turn_start: {self.firing_turn_start}, firing_turn_end: {self.firing_turn_end}, roll: {self.roll}, firing_position: <{self.firing_position}>, firing_direction: <{self.firing_direction}>)"


class WeaponWithCannons(object):
    def __init__(self, scale: Vector3, position: Vector3, orientation: Quaternion,
                 hull_index_parent: int, local_direction: Vector3,
                 cannons: list[Cannon]):
        self.scale             = scale
        self.position          = position
        self.orientation       = orientation
        self.hull_index_parent = int(hull_index_parent)
        self.local_direction   = local_direction
        self.cannons           = cannons
