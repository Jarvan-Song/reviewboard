from django.core.exceptions import ValidationError
    @add_fixtures(['test_scmtools'])
    def test_create_with_site(self):
        """Testing ReviewRequest.objects.create with LocalSite"""
        user = User.objects.get(username='doc')
        local_site = LocalSite.objects.create(name='test')
        repository = self.create_repository()

        review_request = ReviewRequest.objects.create(
            user, repository, local_site=local_site)
        self.assertEqual(review_request.repository, repository)
        self.assertEqual(review_request.local_site, local_site)
        self.assertEqual(review_request.local_id, 1)

    @add_fixtures(['test_scmtools'])
    def test_create_with_site_and_commit_id(self):
        """Testing ReviewRequest.objects.create with LocalSite and commit ID"""
        user = User.objects.get(username='doc')
        local_site = LocalSite.objects.create(name='test')
        repository = self.create_repository()

        review_request = ReviewRequest.objects.create(
            user, repository,
            commit_id='123',
            local_site=local_site)
        self.assertEqual(review_request.repository, repository)
        self.assertEqual(review_request.commit_id, '123')
        self.assertEqual(review_request.local_site, local_site)
        self.assertEqual(review_request.local_id, 1)

    @add_fixtures(['test_scmtools'])
    def test_create_with_site_and_commit_id_not_unique(self):
        """Testing ReviewRequest.objects.create with LocalSite and
        commit ID that is not unique
        """
        user = User.objects.get(username='doc')
        local_site = LocalSite.objects.create(name='test')
        repository = self.create_repository()

        # This one should be fine.
        ReviewRequest.objects.create(user, repository, commit_id='123',
                                     local_site=local_site)
        self.assertEqual(local_site.review_requests.count(), 1)

        # This one will yell.
        self.assertRaises(
            ValidationError,
            lambda: ReviewRequest.objects.create(
                user, repository,
                commit_id='123',
                local_site=local_site))

        # Make sure that entry doesn't exist in the database.
        self.assertEqual(local_site.review_requests.count(), 1)

    @add_fixtures(['test_scmtools'])
    def test_create_with_site_and_commit_id_and_fetch_problem(self):
        """Testing ReviewRequest.objects.create with LocalSite and
        commit ID with problem fetching commit details
        """
        user = User.objects.get(username='doc')
        local_site = LocalSite.objects.create(name='test')
        repository = self.create_repository()

        self.assertEqual(local_site.review_requests.count(), 0)

        ReviewRequest.objects.create(
            user, repository,
            commit_id='123',
            local_site=local_site,
            create_from_commit_id=True)

        # Make sure that entry doesn't exist in the database.
        self.assertEqual(local_site.review_requests.count(), 1)
        review_request = local_site.review_requests.get()
        self.assertEqual(review_request.local_id, 1)
        self.assertEqual(review_request.commit_id, '123')

            self.assertIn(summary, summaries,
            self.assertIn(summary, r_summaries,
    def _get_context_var(self, response, varname):
    def test_review_detail_redirect_no_slash(self):
        """Testing review_detail view redirecting with no trailing slash"""
    def test_review_detail(self):
        """Testing review_detail view"""
        request = self._get_context_var(response, 'review_request')
    def test_review_detail_context(self):
        """Testing review_detail view's context"""
        request = self._get_context_var(response, 'review_request')
        """Testing review_detail and ordering of diff comments on a review"""
    def test_review_detail_sitewide_login(self):
    def test_new_review_request(self):
        """Testing new_review_request view"""
    def test_interdiff(self):
            print("Error: %s" % self._get_context_var(response, 'error'))
            print(self._get_context_var(response, 'trace'))
            self._get_context_var(response, 'diff_context')['num_diffs'],
        files = self._get_context_var(response, 'files')
        self.assertIn('interfilediff', files[0])
        self.assertIn('interfilediff', files[1])
    def test_interdiff_new_file(self):
            print("Error: %s" % self._get_context_var(response, 'error'))
            print(self._get_context_var(response, 'trace'))
            self._get_context_var(response, 'diff_context')['num_diffs'],
        files = self._get_context_var(response, 'files')
        self.assertIn('interfilediff', files[0])
    def test_draft_changes(self):
        draft = self._get_draft()
        self.assertIn("summary", fields)
        self.assertIn("description", fields)
        self.assertIn("testing_done", fields)
        self.assertIn("branch", fields)
        self.assertIn("bugs_closed", fields)
    def _get_draft(self):
    def test_duplicate_reviews(self):
        self.assertIn(default_reviewer1, default_reviewers)
        self.assertIn(default_reviewer2, default_reviewers)
        self.assertIn(default_reviewer2, default_reviewers)
        self.assertIn(default_reviewer1, default_reviewers)
        self.assertIn(default_reviewer2, default_reviewers)
    def test_milestones(self):
    def test_palindrome(self):
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             starred_public=1)
        self._check_counters(total_outgoing=1, pending_outgoing=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             direct_incoming=1,
                             total_incoming=1,
                             starred_public=1,
                             group_incoming=1)
        self.review_request.close(close_type)
        self._check_counters(total_outgoing=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1)

        self._check_counters(total_outgoing=1)
    def test_closing_closed_requests(self):
        """Testing counters with closing closed review requests"""
        # The review request was already created
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1)

        self.assertFalse(self.review_request.public)
        self.assertEqual(self.review_request.status,
                         ReviewRequest.PENDING_REVIEW)

        self.review_request.close(ReviewRequest.DISCARDED)
        self._check_counters(total_outgoing=1)

        self.review_request.close(ReviewRequest.SUBMITTED)
        self._check_counters(total_outgoing=1)
        """Testing counters with closing draft review requests on LocalSite"""

        self._check_counters(with_local_site=True)
        self._check_counters(with_local_site=True,
                             total_outgoing=1,
                             pending_outgoing=1)
        self.review_request.close(ReviewRequest.DISCARDED)
        self._check_counters(with_local_site=True,
                             total_outgoing=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1)
        self.review_request.publish(self.user)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             direct_incoming=1,
                             total_incoming=1,
                             starred_public=1,
                             group_incoming=1)
        self._check_counters()
        # We're simulating what a DefaultReviewer would do by populating
        # the ReviewRequest's target users and groups while not public and
        # without a draft.
        self.review_request.target_people.add(self.user)
        self.review_request.target_groups.add(self.group)

        self._check_counters(total_outgoing=1,
                             pending_outgoing=1)
        self._check_counters()
    def test_deleting_closed_requests(self):
        """Testing counters with deleting closed review requests"""
        # We're simulating what a DefaultReviewer would do by populating
        # the ReviewRequest's target users and groups while not public and
        # without a draft.
        self.review_request.target_people.add(self.user)
        self.review_request.target_groups.add(self.group)

        # The review request was already created
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1)

        self.review_request.close(ReviewRequest.DISCARDED)
        self._check_counters(total_outgoing=1)

        self.review_request.delete()
        self._check_counters()
        self.assertEqual(self.review_request.status,
                         ReviewRequest.PENDING_REVIEW)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             direct_incoming=1,
                             total_incoming=1,
                             starred_public=1,
                             group_incoming=1)
        self.assertEqual(self.review_request.status,
                         ReviewRequest.PENDING_REVIEW)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             direct_incoming=1,
                             total_incoming=1,
                             starred_public=1,
                             group_incoming=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             direct_incoming=1,
                             total_incoming=1,
                             starred_public=1,
                             group_incoming=1)
        self.assertEqual(self.review_request.status,
                         ReviewRequest.PENDING_REVIEW)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1)
        # We're simulating what a DefaultReviewer would do by populating
        # the ReviewRequest's target users and groups while not public and
        # without a draft.
        self.review_request.target_people.add(self.user)
        self.review_request.target_groups.add(self.group)

        self._check_counters(total_outgoing=1)

        self.assertEqual(self.review_request.status,
                         ReviewRequest.PENDING_REVIEW)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             direct_incoming=1,
                             total_incoming=1,
                             starred_public=1,
                             group_incoming=1)

    def test_double_publish(self):
        """Testing counters with publishing a review request twice"""
        self.assertFalse(self.review_request.public)
        self.assertEqual(self.review_request.status,
                         ReviewRequest.PENDING_REVIEW)

        # Publish the first time.
        self.review_request.publish(self.user)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             starred_public=1)

        # Publish the second time.
        self.review_request.publish(self.user)

        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             starred_public=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             total_incoming=1,
                             group_incoming=1,
                             starred_public=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             total_incoming=1,
                             group_incoming=1,
                             starred_public=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             starred_public=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             direct_incoming=1,
                             total_incoming=1,
                             starred_public=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             direct_incoming=1,
                             total_incoming=1,
                             starred_public=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             starred_public=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             total_incoming=1,
                             direct_incoming=1,
                             starred_public=1,
                             group_incoming=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             total_incoming=1,
                             direct_incoming=1,
                             starred_public=1,
                             group_incoming=1)
        self._check_counters(total_outgoing=1,
                             pending_outgoing=1)

        self._check_counters(total_outgoing=1,
                             pending_outgoing=1,
                             direct_incoming=1,
                             total_incoming=1,
                             starred_public=1,
                             group_incoming=1)

    def _check_counters(self, total_outgoing=0, pending_outgoing=0,
                        direct_incoming=0, total_incoming=0,
                        starred_public=0, group_incoming=0,
                        with_local_site=False):

        if with_local_site:
            main_site_profile = self.site_profile2
            unused_site_profile = self.site_profile
        else:
            main_site_profile = self.site_profile
            unused_site_profile = self.site_profile2

        self.assertEqual(main_site_profile.total_outgoing_request_count,
                         total_outgoing)
        self.assertEqual(main_site_profile.pending_outgoing_request_count,
                         pending_outgoing)
        self.assertEqual(main_site_profile.direct_incoming_request_count,
                         direct_incoming)
        self.assertEqual(main_site_profile.total_incoming_request_count,
                         total_incoming)
        self.assertEqual(main_site_profile.starred_public_request_count,
                         starred_public)
        self.assertEqual(self.group.incoming_request_count, group_incoming)

        # These should never be affected by the updates on the main
        # LocalSite we're working with, so they should always be 0.
        self.assertEqual(unused_site_profile.total_outgoing_request_count, 0)
        self.assertEqual(unused_site_profile.pending_outgoing_request_count, 0)
        self.assertEqual(unused_site_profile.direct_incoming_request_count, 0)
        self.assertEqual(unused_site_profile.total_incoming_request_count, 0)
        self.assertEqual(unused_site_profile.starred_public_request_count, 0)
        self.assertIn(group, Group.objects.accessible(self.user))
        self.assertIn(group, Group.objects.accessible(self.anonymous))
        self.assertNotIn(group, Group.objects.accessible(self.user))
        self.assertNotIn(group, Group.objects.accessible(self.anonymous))
        self.assertIn(group, Group.objects.accessible(self.user))
        self.assertNotIn(group, Group.objects.accessible(self.anonymous))
    def test_unicode(self):