from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Table, INTEGER, Text, Column, ForeignKey

Base = declarative_base()

films_planets = Table(
    'films_planets',
    Base.metadata,
    Column("id_films", ForeignKey("Films.id")),
    Column("id_planets", ForeignKey("Planets.id"))
)

films_species = Table(
    'films_species',
    Base.metadata,
    Column("id_films", ForeignKey("Films.id")),
    Column("id_species", ForeignKey("Species.id"))
)

films_starships = Table(
    'films_starships',
    Base.metadata,
    Column("id_films", ForeignKey("Films.id")),
    Column("id_starships", ForeignKey("Starships.id"))
)

films_vehicles = Table(
    'films_vehicles',
    Base.metadata,
    Column("id_films", ForeignKey("Films.id")),
    Column("id_vehicles", ForeignKey("Vehicles.id"))
)

films_people = Table(
    'films_people',
    Base.metadata,
    Column("id_films", ForeignKey("Films.id")),
    Column("id_people", ForeignKey("People.id"))
)

people_starships = Table(
    'people_starships',
    Base.metadata,
    Column("id_people", ForeignKey("People.id")),
    Column("id_starships", ForeignKey("Starships.id"))
)

people_vehicles = Table(
    'people_vehicles',
    Base.metadata,
    Column("id_people", ForeignKey("People.id")),
    Column("id_vehicles", ForeignKey("Vehicles.id"))
)

class Films(Base):
    __tablename__ = "Films"

    id = Column(INTEGER, primary_key = True, autoincrement=True)
    title = Column(Text)
    episode_id = Column(INTEGER)
    opening_crawl = Column(Text)
    director = Column(Text)
    producer = Column(Text)
    release_date = Column(Text)

    f_planets = relationship('Planets', secondary=films_planets, backref='pl_films')
    f_species = relationship('Species', secondary=films_species, backref='sp_films')
    f_starships = relationship('Starships', secondary=films_starships, backref='st_films')
    f_vehicles = relationship('Vehicles', secondary=films_vehicles, backref='vh_films')
    f_people = relationship('People', secondary=films_people, backref='pp_films')

class People(Base):
    __tablename__ = "People"

    id = Column(INTEGER, primary_key = True, autoincrement=True)
    name = Column(Text)
    height = Column(INTEGER)
    mass = Column(Text)
    hair_color = Column(Text)
    skin_color = Column(Text)
    eye_color = Column(Text)
    birth_year = Column(Text)
    gender = Column(Text)
    homeworld = Column(INTEGER, ForeignKey("Planets.id"))
    species = Column(INTEGER, ForeignKey("Species.id"))

    pp_starships = relationship('Starships', secondary=people_starships, backref='st_people')
    pp_vehicles = relationship('Vehicles', secondary=people_vehicles, backref='vh_people')

class Planets(Base):
    __tablename__ = "Planets"

    id = Column(INTEGER, primary_key = True, autoincrement=True)
    name = Column(Text)
    rotation_period = Column(Text)
    orbital_period = Column(Text)
    diameter = Column(Text)
    climate = Column(Text)
    gravity = Column(Text)
    terrain = Column(Text)
    surface_water = Column(Text)
    population = Column(Text)

    pl_people = relationship('People', backref="pp_planets")
    pl_species = relationship('Species', backref='sp_planets')
    
class Species(Base):
    __tablename__ = "Species"

    id = Column(INTEGER, primary_key = True, autoincrement=True)
    name = Column(Text)
    classification = Column(Text)
    designation = Column(Text)
    average_height = Column(Text)
    skin_colors = Column(Text)
    hair_colors = Column(Text)
    eye_colors = Column(Text)
    average_lifespan = Column(Text)
    homeworld = Column(INTEGER, ForeignKey('Planets.id'))
    language = Column(Text)

    sp_people = relationship('People', backref='pp_species')

class Starships(Base):
    __tablename__ = "Starships"

    id = Column(INTEGER, primary_key = True, autoincrement=True)
    name = Column(Text)
    model = Column(Text)
    manufacturer = Column(Text)
    cost_in_credits = Column(Text)
    length = Column(Text)
    max_atmosphering_speed = Column(Text)
    crew = Column(Text)
    passengers = Column(Text)
    cargo_capacity = Column(INTEGER)
    consumables = Column(Text)
    hyperdrive_rating = Column(Text)
    MGLT = Column(Text)
    starship_class = Column(Text)

class Vehicles(Base):
    __tablename__ = "Vehicles"

    id = Column(INTEGER, primary_key = True, autoincrement=True)
    name = Column(Text)
    model = Column(Text)
    manufacturer = Column(Text)
    cost_in_credits = Column(Text)
    length = Column(Text)
    max_atmosphering_speed = Column(Text)
    crew = Column(Text)
    passengers = Column(Text)
    cargo_capacity = Column(INTEGER)
    consumables = Column(Text)
    vehicle_class = Column(Text)