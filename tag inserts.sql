-- SQLite
alter table tag
rename to tag_old;

create table tag (
	id integer primary key not null,
	name string not null unique,
	desc string 
);

insert into tag select * from tag_old

drop table tag_old;

delete from tag;

insert into tag values(1, "None", "Default value. Pick this if you do not want your project to be tagged. (Excludes it from tag-search)");

insert into tag values (2, "Art", "Artworks or software aimed at the creation thereof");

insert into tag values(3, "Social", "Social engineering software and other socially-oriented works");

insert into tag values(4, "Data", "Data science software or projects that revolve around data");

insert into tag values(5, "Library", "Independent libraries or contributions to pre-existing third-party libraries");

insert into tag values(6, "Meta", "Contributions to the CPython distribution");

insert into tag values(7, "Other", "Projects written in languages other than Python or that refuse categorization (edgy)");

insert into tag values(1, "None", "Default value. Pick this if you do not want your project to be tagged. (Excludes it from tag-search)")

-- TODO: Comment this code