/* License: GPL */
/* Copyright: Mandriva */

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <grp.h>
#include <pwd.h>
#include <string.h>

int main(int argc, char *argv[])
{
	int i = 0;
	int ng = 1;
	char *user;
	gid_t *groups = NULL;
	gid_t gid;
	struct group *mygroup = NULL;
	struct passwd *pw = NULL;

	if (argc != 2) {
		printf("\nLists the groups a given username is part of using the getgrouplist(3) function.\n");
		printf("Usage: %s <username>\n\n", argv[0]);
		exit(1);
	}

	user = strdup(argv[1]);
	if ((pw = getpwnam(user)) == NULL) {
		printf("Error: user '%s' doesn't exist.\n", user);
		exit(1);
	}

	if ((groups = (gid_t *) malloc(ng * sizeof(gid_t))) == NULL) {
		printf("Error, out of memory.\n");
		exit(1);
	}
	
	if (getgrouplist(user, pw->pw_gid, groups, &ng) == -1) {
		/* use realloc... */
		free(groups);
		groups = malloc((size_t)(ng * sizeof(gid_t)));
		if (groups == NULL) {
			printf("Error, out of memory.\n");
			exit(1);
		}
		if (getgrouplist(user, pw->pw_gid, groups, &ng) == -1) {
			printf("getgrouplist(): error fetching list of groups.\n");
			exit(1);
		}
	}

	for(i = 0; i < ng; i++) {
		mygroup = getgrgid(groups[i]);
		if (mygroup != NULL)
			printf("%s", mygroup->gr_name);
		else
			continue;
		if (i < ng - 1)
			printf(",");
		else
			printf("\n");
	}
	free(groups);
	free(user);
	return 0;
}

